# RIP

Юлдашев Кирилл КН-202 n=24

## Настройка

1. Назначим на комп-ах IP в соответсвии с таблицей, шлюз по умолчанию для PC0 и PC1 выберем Router1, соединим всё соответствующими проводами (для устр-в разных уровней модели OSI - прямой, для устр-в одинаковых уровней - перекрёстный); добавим плату с разъёмами на каждый роутер, назначим IP для интерфейсов в соответсвии с таблицами (Я делал это в поле Config-INTERFACE, можно было писать вручную в CLI)

2. Теперь нужно настроить RIP, для этого в поле CLI для каждого роутера напишем :

   1. configure terminal
   2. router rip
   3. network <классовая сеть>

   (Либо, в поле Config-RIP сделать то же самое)

   ## Таблички маршрутизации и информация по всем интерфейсам

   ### Router 1:

   ```
   Router>show ip route
   Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
          D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
          N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
          E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
          i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
          * - candidate default, U - per-user static route, o - ODR
          P - periodic downloaded static route

   Gateway of last resort is not set

        10.0.0.0/24 is subnetted, 1 subnets
   C       10.24.1.0 is directly connected, FastEthernet0/1
   C    192.168.1.0/24 is directly connected, Ethernet1/0
        192.168.10.0/30 is subnetted, 2 subnets
   C       192.168.10.0 is directly connected, FastEthernet0/0
   R       192.168.10.4 [120/1] via 192.168.10.2, 00:00:03, FastEthernet0/0

   Router>show ip interface brief
   Interface              IP-Address      OK? Method Status                Protocol 
   FastEthernet0/0        192.168.10.1    YES manual up                    up 
   FastEthernet0/1        10.24.1.1       YES manual up                    up 
   Ethernet1/0            192.168.1.1     YES manual up                    up 
   Vlan1                  unassigned      YES unset  administratively down down
   ```

### Router 2:

```
Router>show ip route
Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

R    10.0.0.0/8 [120/1] via 192.168.10.5, 00:00:20, FastEthernet0/1
                [120/1] via 192.168.10.1, 00:00:14, FastEthernet0/0
R    192.168.1.0/24 [120/1] via 192.168.10.1, 00:00:14, FastEthernet0/0
C    192.168.2.0/24 is directly connected, Ethernet1/0
     192.168.10.0/30 is subnetted, 2 subnets
C       192.168.10.0 is directly connected, FastEthernet0/0
C       192.168.10.4 is directly connected, FastEthernet0/1

Router>show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol 
FastEthernet0/0        192.168.10.2    YES manual up                    up 
FastEthernet0/1        192.168.10.6    YES manual up                    up 
Ethernet1/0            192.168.2.1     YES manual up                    up 
Vlan1                  unassigned      YES unset  administratively down down
```

### Router 3:

```
Router>show ip route
Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

     10.0.0.0/24 is subnetted, 1 subnets
C       10.24.1.0 is directly connected, FastEthernet0/0
R    192.168.1.0/24 [120/1] via 10.24.1.1, 00:00:26, FastEthernet0/0
C    192.168.3.0/24 is directly connected, Ethernet1/0
     192.168.10.0/30 is subnetted, 2 subnets
R       192.168.10.0 [120/1] via 192.168.10.6, 00:00:07, FastEthernet0/1
C       192.168.10.4 is directly connected, FastEthernet0/1

Router>show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol 
FastEthernet0/0        10.24.1.2       YES manual up                    up 
FastEthernet0/1        192.168.10.5    YES manual up                    up 
Ethernet1/0            192.168.3.1     YES manual up                    up 
Vlan1                  unassigned      YES unset  administratively down down
```

P.S. сами IP и маски подписаны рядом с комп-ами и серверами в самой работе (.pkt файле)

