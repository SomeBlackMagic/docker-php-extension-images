on arm node
```bash

apt install -y docker.io docker-buildx
nano /root/.ssh/authorized_keys 

```


# on amd node
- install php pkg
- install docker and buildx
- generate ssh key
```bash

apt install docker-buildx

docker buildx create \
--name local_remote_builder \
--node amd \
--platform linux/amd64,linux/386,linux/riscv64,linux/ppc64le,linux/s390x,linux/mips64le,linux/mips64 \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SIZE=10000000 \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SPEED=10000000

ssh -o ConnectTimeout=30 -l root -- 37.27.244.168 <--- approve host key


docker buildx create \
--name local_remote_builder  \
--append  \
--node arm  \
--platform linux/arm/v8,linux/arm/v7,linux/arm/v6,linux/arm64  \
ssh://root@37.27.244.168  \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SIZE=10000000  \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SPEED=10000000 
```

```bash

php bin/console render 7.4 glibc
php bin/console render 7.4 musl


php bin/console render 8.0 glibc
php bin/console render 8.0 musl


php bin/console render 8.1 glibc
php bin/console render 8.1 musl

php bin/console render 8.2 glibc
php bin/console render 8.2 musl

php bin/console render 8.3 glibc
php bin/console render 8.3 musl

php bin/console render 8.4 glibc
php bin/console render 8.4 musl



bash docker-php-extension-images/dst/builder-7.4-glibc.sh
bash docker-php-extension-images/dst/builder-7.4-musl.sh


bash docker-php-extension-images/dst/builder-8.0-glibc.sh
bash docker-php-extension-images/dst/builder-8.0-musl.sh


bash docker-php-extension-images/dst/builder-8.1-glibc.sh
bash docker-php-extension-images/dst/builder-8.1-musl.sh

bash docker-php-extension-images/dst/builder-8.2-glibc.sh
bash docker-php-extension-images/dst/builder-8.2-musl.sh

bash docker-php-extension-images/dst/builder-8.3-glibc.sh
bash docker-php-extension-images/dst/builder-8.3-musl.sh

bash docker-php-extension-images/dst/builder-8.4-glibc.sh
bash docker-php-extension-images/dst/builder-8.4-musl.sh


```
