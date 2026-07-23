# -------------------- Installing PHP Extension: imap --------------------
RUN set -eux \
    && install-php-extensions imap \
    && php -m | grep -oiE '^imap$' \
    && true
