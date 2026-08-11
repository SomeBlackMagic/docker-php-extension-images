FROM php:{{ version }}-{{ base_os }}

RUN set -eux \
    && apk upgrade --available \
    && apk add curl autoconf build-base autoconf automake git gcc make g++  \
    && true

{% for image_tag in image_tags %}COPY --from={{ image_tag }} / /
{% endfor %}
###
### Verify
###
RUN set -eux \
    && echo "date.timezone=UTC" > /usr/local/etc/php/php.ini \
    && php -v | grep -oE 'PHP\s[.0-9]+' | grep -oE '[.0-9]+' | grep '^{{ version }}' \
    \
    && PHP_ERROR="$( php -v 2>&1 1>/dev/null )" \
    && if [ -n "${PHP_ERROR}" ]; then echo "${PHP_ERROR}"; false; fi \
    && PHP_ERROR="$( php -i 2>&1 1>/dev/null )" \
    && if [ -n "${PHP_ERROR}" ]; then echo "${PHP_ERROR}"; false; fi \
    \
    && rm -f /usr/local/etc/php/php.ini \
    && true
