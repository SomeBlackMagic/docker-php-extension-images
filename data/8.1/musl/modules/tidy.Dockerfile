# -------------------- Installing PHP Extension: tidy --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
#    && apk add tidyhtml-dev \
    && install-php-extensions tidy \
    && php -m | grep -oiE '^tidy$' \
    && true
