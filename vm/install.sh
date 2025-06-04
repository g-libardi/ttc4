sudo apt-get update
sudo apt-get install -y gcc python-pip unzip inetutils-traceroute iperf3

git clone https://github.com/mininet/mininet.git
./mininet/util/install.sh
pip install mininet

echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv6.conf.all.forwarding=1' | sudo tee -a /etc/sysctl.conf