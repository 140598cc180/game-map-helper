plugins {
    id("com.android.application")
}

android {
    namespace = "com.cici.identityvmaphelper"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.cici.identityvmaphelper"
        minSdk = 28
        targetSdk = 35
        versionCode = 2
        versionName = "2.0.0-phone-web"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
