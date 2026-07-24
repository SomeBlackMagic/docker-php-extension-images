#COPY --from=someblackmagic/docker-php-extension-images:7.4-raphf-glibc / /
#COPY --from=someblackmagic/docker-php-extension-images:7.4-propro-glibc / /

# -------------------- Installing PHP Extension: http --------------------
RUN set -eux \
    && install-php-extensions http \
    && php -m | grep -oiE '^http$' \
    && true


