package com.example.myapplication.cropdisease;


import okhttp3.MultipartBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface ApiService {

    @POST("predict") // The endpoint on your backend
    Call<PredictionResponse> uploadImage(@Part MultipartBody.Part image);
}
