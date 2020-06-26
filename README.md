# Jetson Nano based person following bot
본 repository에는 Jetson Nano와 JetPack에 포함된 Object Detecion 모델인 SSD를 이용하여 간단한 Person Following bot을 만드는 과정과 방법이 기록되어 있다. 필자는 Jetson Nano를 이용하였지만, XAVIER등의 다른 Jetson 보드에서도 작동이 가능할 것으로 생각된다. 여기서는 Nano를 기준으로 설명한다.
## OS Installation
Jetson Nano를 사용하기 위해서는 JetPack이라고 불리는 OS를 보드에 설치해야 한다.  JetPack은 [이 링크](https://developer.nvidia.com/embedded/jetpack)에서 다운로드 받을 수 있다. 각자의 보드에 맞는 JetPack을 다운로드 받아 [Etcher](https://www.balena.io/etcher/), [Rufus](https://rufus.ie/)와 같은 툴을 이용하여 Jetson 보드의 SD카드에 플래시해 준다. 이후 처음 부팅시 뜨는 안내에 따라 초기설정을 진행하면 된다. 언어 설정은 **영어**로 하는것을 추천.

## HW
Jetson Nano 와 L298N 모터드라이버, 저렴한 아두이노 DC모터를 이용하였다. 정방향으로만 움직이게 할 생각이므로 L298N의  IN2, IN4에 5V를 직접 연결하였다. 물론 이는 모터의 방향과 순서에 따라 다르게 연결해야 할 것이다. 이외 배선 연결은 간단하므로 따로 설명하지 않겠다.

## SW
Ctrl+Alt+T를 눌러 터미널 창을 하나 띄우고 다음과 같이 입력한다.

    sudo apt-get update
    sudo apt-get install git cmake libpython3-dev python3-numpy
    git clone --recursive https://github.com/dusty-nv/jetson-inference
    cd jetson-inference
    mkdir build
    cd build
    cmake ../
    
  한줄씩 입력하여 작업이 완료되면 다음 줄을 입력한다 . 마지막줄을 입력하면 아래와 같은 창이 뜬다. 
  ![](https://raw.githubusercontent.com/dusty-nv/jetson-inference/python/docs/images/download-models.jpg)
꼭 필요한 것은 Object Detection의 SSD-Mobilenet-v2이므로 이것만 체크하고 Ok를 눌러 진행해도 무방하다. 다른 Model을 사용해 보고 싶다면 사용할 것을 체크하여 진행하면 된다.

Model 다운로드가 완료된 후 아래와 같은 Pytorch 설치화면이 뜨는데 Pytorch 또한 꼭 필요한 것은 아니므로 개인적으로 필요한 사람만 선택하여 설치하면 된다.
![](https://raw.githubusercontent.com/dusty-nv/jetson-inference/python/docs/images/pytorch-installer.jpg)
다시 아래와 같이 명령어들을 입력한다.

    make
    sudo make install
    sudo ldconfig
이후 PWM을 사용하기 위해 다음과 같이 입력한다.

    # 32번 핀을 PWM0로 설정 
    busybox devmem 0x700031fc 32 0x45
    busybox devmem 0x6000d504 32 0x2
    
    # 33번 핀을 PWM2로 설정
    busybox devmem 0x70003248 32 0x46
    busybox devmem 0x6000d100 32 0x00

여기까지 에러 없이 잘 진행했다면 기본적인 초기설정은 완료하였다.

    git clone https://github.com/kemjensak/jetson-nano-person-following-bot
    cd jetson-nano-person-following-bot
이제 다음 명령어를 입력하면 로딩 후 모터가 돌기 시작할 것이다.

    python3 run.py

## Future
위에서 사용한 파이썬 코드는 단순히 사람으로 인식된 Bounding Box를 화면의 가운데로 오도록 하는 기본적인 코드이다. 추후 여러 사람이 인식되었을 경우에도 한 사람만 따라가도록 할 수 있게, 특정 거리범위 내에서만 따라가게 하는 기능을 구현해 볼 예정이다.

