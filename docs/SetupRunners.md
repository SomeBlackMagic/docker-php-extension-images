On x86 cloud init 
```
#cloud-config
package_update: true
packages:
  - mc
  - htop
  - iftop
  - iotop
  - pv
  - ncdu
  - git
  - docker.io
  - docker-buildx
  - php-cli
  - composer
runcmd:
  - git clone https://github.com/SomeBlackMagic/docker-php-extension-images.git /root/docker-php-extension-images
  - cd /root/docker-php-extension-images && git config pull.rebase true
  - ssh-keygen -t ed25519 -f /root/.ssh/id_ed25519 -N ""

```

```bash
cat /root/.ssh/id_ed25519.pub

```
on arm node
```bash
nano /root/.ssh/authorized_keys 

docker buildx create \
--name local_remote_builder \
--node amd \
--platform linux/amd64,linux/386,linux/riscv64,linux/ppc64le,linux/s390x,linux/mips64le,linux/mips64 \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SIZE=10000000 \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SPEED=10000000

ssh -o ConnectTimeout=30 -l root -- 157.180.92.19 <--- approve host key

docker buildx create \
--name local_remote_builder  \
--append  \
--node arm  \
--platform linux/arm64  \
ssh://root@157.180.92.19  \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SIZE=10000000  \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SPEED=10000000 

docker buildx use local_remote_builder
```


docker buildx create \
--name local_remote_builder \
--append \
--node arm \
--platform linux/arm64 \
ssh://a_cherniy@91.225.161.158:35000 \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SIZE=10000000 \
--driver-opt env.BUILDKIT_STEP_LOG_MAX_SPEED=10000000


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



find ./ -type f -exec sed -i '' 's#\-\-push# #' *.sh {} \;
