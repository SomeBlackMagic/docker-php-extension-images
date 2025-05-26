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


