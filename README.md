# Motion

A simple motion detection application that saves images from a webcam when movement is detected.

## How to Run

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
