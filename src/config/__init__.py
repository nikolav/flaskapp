import os
import re

from dotenv import load_dotenv


load_dotenv()


ENV_ = os.getenv('ENV')
DEVELOPMENT_ = 'development' == ENV_
PRODUCTION_  = 'production'  == ENV_

class Config:

  ENV         = ENV_
  DEVELOPMENT = DEVELOPMENT_
  PRODUCTION  = PRODUCTION_
  PORT        = os.getenv('PORT')
  APP_NAME    = os.getenv('APP_NAME')
  
  SECRET_KEY = os.getenv('SECRET_KEY')
  
  MESSAGE = os.getenv('MESSAGE')
  
  # keys
  KEY_TOKEN_CREATED_AT     = '@'
  AUTH_PROFILE             = os.getenv('AUTH_PROFILE')
  CLOUD_MESSAGING_TOKENS   = os.getenv('CLOUD_MESSAGING_TOKENS')
  COLLECTIONS_DOCS_UPDATED = os.getenv('COLLECTIONS_DOCS_UPDATED')
  
  # paths
  FLASK_TEMPLATES_FOLDER     = os.getenv('FLASK_TEMPLATES_FOLDER')
  CATEGORY_KEY_ASSETS_prefix = os.getenv('CATEGORY_KEY_ASSETS_prefix')

  # cache:redis
  REDIS_INIT = bool(os.getenv('REDIS_INIT'))
  REDIS_URL  = os.getenv('REDIS_URL')

  # io:cors
  IO_CORS_ALLOW_ORIGINS = re.split(r'\s+', os.getenv('IO_CORS_ALLOW_ORIGINS').strip())

  # io
  IOEVENT_REDIS_CACHE_KEY_UPDATED_prefix = os.getenv('IOEVENT_REDIS_CACHE_KEY_UPDATED_prefix')
  
  # jwt
  JWT_EXPIRE_SECONDS      = int(os.getenv('JWT_EXPIRE_SECONDS'))
  JWT_SECRET_ACCESS_TOKEN = os.getenv('JWT_SECRET_ACCESS_TOKEN')

  # db:mongo
  MONGODB_INIT = bool(os.getenv('MONGODB_INIT'))
  MONGODB_URI = os.getenv('MONGODB_URI_production') if PRODUCTION_ else os.getenv('MONGODB_URI_development')

  # cloud messaging
  FIREBASEADMIN_INIT           = bool(os.getenv('FIREBASEADMIN_INIT'))
  CERTIFICATE_FIREBASEADMINSDK = os.getenv('CERTIFICATE_FIREBASEADMINSDK')

  # db
  DB_INIT                        = bool(os.getenv('DB_INIT'))
  DATABASE_URI_development       = os.getenv('DATABASE_URI_development')
  DATABASE_URI_production        = os.getenv('DATABASE_URI_production')
  TABLE_NAME_SUFFIX_dev          = os.getenv('TABLE_NAME_SUFFIX_dev')
  TABLE_NAME_SUFFIX_production   = os.getenv('TABLE_NAME_SUFFIX_production')
  SQLALCHEMY_ECHO                = bool(os.getenv('SQLALCHEMY_ECHO'))
  SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
  REBUILD_SCHEMA                 = bool(os.getenv('REBUILD_SCHEMA'))
  
  # auth
  PATHS_SKIP_AUTH = (
    r'^/$',
    r'^/auth/authenticate$',

    # webhook:viber
    r'^/webhook_viber_channel/.*',

    # webhook:any
    r'^/webhook/.*',
  )
  
  # mail
  mail = {
    'HOST'         : os.getenv('EMAIL_SERVER'),
    'PORT'         : int(os.getenv('EMAIL_SERVER_PORT')),
    'USER'         : os.getenv('EMAIL_USER'),
    'PASSWORD'     : os.getenv('EMAIL_PASSWORD'),
    'EMAIL_SENDER' : os.getenv('EMAIL_DEFAULT_SENDER'),
  }

  # viber
  VIBER_CHANNELS_CACHE_KEY        = 'viber_channels'
  VIBER_CHANNELS_SET_WEBHOOK_URL  = os.getenv('VIBER_CHANNELS_SET_WEBHOOK_URL')
  VIBER_CHANNELS_ACCOUNT_INFO_URL = os.getenv('VIBER_CHANNELS_ACCOUNT_INFO_URL')
  VIBER_CHANNELS_POST_MESSAGE_URL = os.getenv('VIBER_CHANNELS_POST_MESSAGE_URL')
  # VIBER_CHANNELS_CACHEID          = os.getenv('VIBER_CHANNELS_CACHEID')

  # aws
  AWS_SESSION_INIT      = bool(os.getenv('AWS_SESSION_INIT'))
  AWS_ACCESS_KEY_ID     = os.getenv('AWS_ACCESS_KEY_ID')
  AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
  AWS_REGION_NAME       = os.getenv('AWS_REGION_NAME')
  
  # uploads
  UPLOADS_MAX_FILENAME_LENGTH = 1024
  UPLOADS_ALLOW_CONTENT_TYPES = {
    # ── Images ─────────────────────────────
    'image/jpeg',
    'image/png',
    'image/webp',
    'image/gif',
    'image/svg+xml',
    'image/heic',          # iOS photos
    'image/heif',

    # ── Documents ──────────────────────────
    'application/pdf',
    'text/plain',
    'text/markdown',

    # Microsoft Office
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',

    # OpenDocument (LibreOffice)
    'application/vnd.oasis.opendocument.text',
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.oasis.opendocument.presentation',

    # ── Archives ───────────────────────────
    'application/zip',
    'application/x-zip-compressed',
    'application/x-tar',
    'application/gzip',
    'application/x-7z-compressed',
    'application/x-rar-compressed',

    # ── Audio ──────────────────────────────
    'audio/mpeg',          # mp3
    'audio/wav',
    'audio/ogg',
    'audio/webm',
    'audio/aac',

    # ── Video ──────────────────────────────
    'video/mp4',
    'video/webm',
    'video/quicktime',     # .mov (iOS)
    'video/x-matroska',    # .mkv

    # ── Data / Web ─────────────────────────
    'application/json',
    'text/csv',
    'application/xml',
    'text/xml',

    # ── Fonts (for web assets) ─────────────
    'font/woff',
    'font/woff2',
    'application/font-woff',
    'application/font-woff2',
    'application/vnd.ms-fontobject',
    'font/ttf',
    'font/otf',

    # ── Generic fallback (use sparingly) ───
    'application/octet-stream',
  }
  UPLOADS_MIME_ALIASES = {
    # ── Images ─────────────────────────────
    'image/jpg': 'image/jpeg',
    'image/pjpeg': 'image/jpeg',          # legacy IE
    'image/x-png': 'image/png',            # legacy

    # iOS / HEIC oddities
    'image/heic-sequence': 'image/heic',
    'image/heif-sequence': 'image/heif',

    # ── Audio ──────────────────────────────
    'audio/mp3': 'audio/mpeg',
    'audio/x-mp3': 'audio/mpeg',
    'audio/mpeg3': 'audio/mpeg',

    # ── Video ──────────────────────────────
    'video/m4v': 'video/mp4',
    'video/x-m4v': 'video/mp4',
    'video/quicktime': 'video/quicktime',  # keep canonical

    # ── Text / Data ────────────────────────
    'text/json': 'application/json',
    'application/x-json': 'application/json',
    'text/xml': 'application/xml',

    # CSV variants
    'application/csv': 'text/csv',
    'text/x-csv': 'text/csv',

    # ── Archives ───────────────────────────
    'application/x-zip': 'application/zip',
    'application/x-zip-compressed': 'application/zip',

    # ── Generic fallbacks (use carefully) ──
    'binary/octet-stream': 'application/octet-stream',
  }
  AWS_UPLOAD_S3_BUCKET = os.getenv('AWS_UPLOAD_S3_BUCKET')
  AWS_UPLOAD_S3_PREFIX = os.getenv('AWS_UPLOAD_S3_PREFIX')
