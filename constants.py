GCP_BUCKET = 'call-center-bucket'
GCP_SERVICE_ACCOUNT_CREDENTIALS = "./gcp-key-for-ai-call-center.json"
CONFIG = {
    "encoding": "MP3",
    "language_code": 'en-US',
    'model': 'telephony',
    "sample_rate_hertz": 8000,
    "enable_speaker_diarization":True,
     "diarization_speaker_count":2,
#     "diarization_config": diarization_config
}