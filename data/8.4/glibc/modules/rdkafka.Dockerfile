# -------------------- Installing PHP Extension: rdkafka --------------------
RUN set -eux \
    && install-php-extensions rdkafka \
    && php -m | grep -oiE '^rdkafka$' \
    && true
