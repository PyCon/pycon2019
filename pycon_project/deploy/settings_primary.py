SITE_ID = 3

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 0  # 15768000  # @@@ Set this to the Larger Value Once We Are Sure this Works
SECURE_FRAME_DENY = True
#SECURE_CONTENT_TYPE_NOSNIFF = True  # @@@ This would be more secure. But I'm not entirely sure of the ramifications

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
