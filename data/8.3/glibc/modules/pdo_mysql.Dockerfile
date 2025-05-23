# -------------------- Installing PHP Extension: pdo_mysql --------------------
RUN set -eux \
    && install-php-extensions pdo_mysql \
    && php -m | grep -oiE '^pdo_mysql$' \
    && true
