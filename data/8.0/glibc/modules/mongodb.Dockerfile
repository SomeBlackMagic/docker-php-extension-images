# -------------------- Installing PHP Extension: mongodb --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command    && apt install -y libicu-dev libsasl2-dev libsnappy-dev libssl-dev \
    && apt update && apt install -y zlib1g-dev libssl-dev libsasl2-dev \
    && pecl install mongodb-1.16.0 \
    # Enabling
    && docker-php-ext-enable mongodb \
    && php -m | grep -oiE '^mongodb$' \
    && true
