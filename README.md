#### LAUNCHING
1. **Download project to your computer**
```Bash
git clone https://github.com/OleksandrLubinskij/DeliPicAPI
cd DeliPicAPI
```
2. **Create .env file in project root**
```Bash
# Database (PostgreSQL)
DB_NAME=delipic_db                  # Name of your PostgreSQL database
DB_USER=postgres                    # Database username
DB_PASSWORD=your_strong_password    # Database user password

# S3 Storage (Cloudflare R2 / AWS S3 / MinIO)
S3_BUCKET_NAME=delipic-images       # Name of the bucket for storing images
S3_ENDPOINT_URL=https://<ACCOUNT_ID>.r2.cloudflarestorage.com  # S3 API endpoint URL from your storage settings
S3_ACCESS_KEY=your_access_key_id    # Access Key ID from your storage API token
S3_SECRET_KEY=your_secret_access_key # Secret Access Key from your storage API token
S3_PUBLIC_URL=https://pub-<HASH>.r2.dev  # Public domain/URL for direct access to uploaded files

# Google Gemini AI
GEMINY_API_KEY=AIzaSy...            # API key generated in Google AI Studio
```
	
3. **Run with Docker**
   - First launch(build the image) 
```Bash
docker compose up --build
```

- Subsequent launches
```Bash
docker compose up
```

- Shutdown the containers
```Bash
docker compose down
```

4. **Make database migrations**
```Bash
docker compose exec backend alembic upgrade head
```

Once running, the API documentation (Swagger UI) will be available at `http://localhost:8002/docs`.
##### Optional: Local environment setup (for IDE autocomplete / running without Docker)
```Bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
```
