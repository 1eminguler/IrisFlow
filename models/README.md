# Models

Model files are **not** committed (they are large binaries, see `.gitignore`).

## Face Landmarker (required for the real engine)

Download `face_landmarker.task` into this folder:

https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task

PowerShell:

```powershell
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task" -OutFile "models/face_landmarker.task"
```

The mock engine (`python -m irisflow --mock`) does not need any model.
