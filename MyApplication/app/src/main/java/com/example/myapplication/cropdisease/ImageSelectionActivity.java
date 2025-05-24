package com.example.myapplication.cropdisease;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import java.io.File;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ImageSelectionActivity extends AppCompatActivity {

    private static final int PICK_IMAGE_REQUEST = 1;

    private ImageView imageView;
    private TextView resultText;
    private Button uploadBtn;

    private Uri imageUri;
    private File imageFile;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_selection);

        imageView = findViewById(R.id.imageView);
        resultText = findViewById(R.id.resultText);
        uploadBtn = findViewById(R.id.uploadBtn);

        // When user clicks on image
        imageView.setOnClickListener(v -> openImageChooser());

        // When user clicks on upload
        uploadBtn.setOnClickListener(v -> {
            if (imageFile != null) {
                uploadImageToServer();
            } else {
                Toast.makeText(this, "Please select an image first", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void openImageChooser() {
        Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(intent, PICK_IMAGE_REQUEST);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == PICK_IMAGE_REQUEST && resultCode == RESULT_OK && data != null) {
            imageUri = data.getData();
            imageView.setImageURI(imageUri);

            // Convert URI to File
            imageFile = FileUtils.getFileFromUri(this, imageUri);
        }
    }

    private void uploadImageToServer() {
        RequestBody requestFile = RequestBody.create(MediaType.parse("image/*"), imageFile);
        MultipartBody.Part body = MultipartBody.Part.createFormData("image", imageFile.getName(), requestFile);

        ApiService apiService = RetrofitClient.getInstance().create(ApiService.class);
        Call<PredictionResponse> call = apiService.uploadImage(body);

        call.enqueue(new Callback<PredictionResponse>() {
            @Override
            public void onResponse(Call<PredictionResponse> call, Response<PredictionResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    resultText.setText("Prediction: " + response.body().getPrediction());
                } else {
                    resultText.setText("Prediction failed.");
                }
            }

            @Override
            public void onFailure(Call<PredictionResponse> call, Throwable t) {
                resultText.setText("Error: " + t.getMessage());
            }
        });
    }
}
