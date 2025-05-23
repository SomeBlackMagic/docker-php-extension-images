# -------------------- Installing PHP Extension: amqp --------------------
RUN set -eux \
    && install-php-extensions amqp \
    && php -m | grep -oiE '^amqp$' \
    && true
