# Motion

A simple motion detection application that saves images from a webcam when movement is detected.

## Configuration

Configuration is managed via environment variables.

1.  Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```
2.  Edit the `.env` file to customize the settings.

### Environment Variables

*   `MOTION_THRESHOLD`: The amount of pixel change that triggers motion detection. Default: `1000`.
*   `SAVE_COOLDOWN_SECONDS`: The minimum time in seconds between saving images. Default: `1`.
*   `OUTPUT_DIR`: The directory inside the container where images are saved. Default: `/data`.
*   `CAMERA_INDEX`: The index of the camera to use. Default: `0`.

## How to Run

First, set up your configuration by creating a `.env` file as described above.

### Release
```bash
docker-compose up -d
```

### Debug
1. Start the debug container:
   ```bash
   docker-compose -f docker-compose-debug.yml up -d
   ```
2. In VS Code, run the `Docker Attach` debug configuration (F5).