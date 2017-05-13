FROM                        ubuntu:14.04
MAINTAINER                  John Else <john.else@gmail.com>

RUN     apt-get update
RUN     apt-get -y install python python-pip sqlite3

RUN     pip install bottle bottle-sqlite

VOLUME  ["/eurovoter"]

COPY    init_container.sh /usr/local/bin

EXPOSE  8080

RUN     useradd eurovoter
RUN     mkdir /home/eurovoter
RUN     chown eurovoter:eurovoter /home/eurovoter

USER    eurovoter
WORKDIR /home/eurovoter

CMD     ["/usr/local/bin/init_container.sh"]
