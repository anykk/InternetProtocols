# Задание для практического занятия по теме DNS

## Юлдашев Кирилл КН-202

**2. Работая с nslookup в режиме одного запроса, выясните адреса серверов имён (NS) для:**

- urfu.ru

  ```
   > urfu.ru.
  ╤хЁтхЁ:  UnKnown
  Address:  192.168.0.1

  Не заслуживающий доверия ответ:
  urfu.ru nameserver = ns1.urfu.ru
  urfu.ru nameserver = ns3.urfu.ru
  urfu.ru nameserver = ns2.urfu.ru

  ns1.urfu.ru     internet address = 212.193.66.21
  ns2.urfu.ru     internet address = 212.193.82.21
  ns3.urfu.ru     internet address = 212.193.72.21
  ```

- msu.ru

  ```
  > msu.ru.
  ╤хЁтхЁ:  UnKnown
  Address:  192.168.0.1

  Не заслуживающий доверия ответ:
  msu.ru  nameserver = ns1.orc.ru
  msu.ru  nameserver = ns.msu.ru
  msu.ru  nameserver = ns3.nic.fr
  msu.ru  nameserver = ns.msu.net

  ns.msu.ru       internet address = 93.180.0.1
  ```

  **выясните ip-адреса хостов для символьных имён:**

- urfu.ru

```
 > urfu.ru.
 ╤хЁтхЁ:  UnKnown
 Address:  192.168.0.1

 Не заслуживающий доверия ответ:
 ╚ь :     urfu.ru
 Address:  212.193.82.20
```

- rbc.ru

```
 > rbc.ru.
 ╤хЁтхЁ:  UnKnown
 Address:  192.168.0.1

 Не заслуживающий доверия ответ:
 ╚ь :     rbc.ru
 Addresses:  185.72.229.9
           80.68.253.9
```

**3. Перейти в режим командной строки nslookup. Выяснить имя и адрес dns-сервера, которому будут отправляться запросы:**

Пример для msu.ru

```
> msu.ru.
╤хЁтхЁ:  A.ROOT-SERVERS.NET
Addresses:  2001:503:ba3e::2:30
          198.41.0.4
# Выше можем видеть текущий сервер (по умолчанию)
╚ь :     msu.ru
Served by:
- a.dns.ripn.net
          193.232.128.6
          2001:678:17:0:193:232:128:6
          ru
- b.dns.ripn.net
          194.85.252.62
          2001:678:16:0:194:85:252:62
          ru
- d.dns.ripn.net
          194.190.124.17
          2001:678:18:0:194:190:124:17
          ru
- e.dns.ripn.net
          193.232.142.17
          2001:678:15:0:193:232:142:17
          ru
- f.dns.ripn.net
          193.232.156.17
          2001:678:14:0:193:232:156:17
          ru
```

**4. Изучить команды перехода между серверами – server, lserver и root**

Установим текущим сервером "194.226.235.1":

```
> server 194.226.235.1
╤хЁтхЁ яю єьюыўрэш■:  [194.226.235.1]
Address:  194.226.235.1
```

Когда попытаемся поменять сервер с помощью server на "ns1.urfu.ru" увидим, что сделать этого мы не можем

```
> server ns1.urfu.ru
DNS request timed out.
    timeout was 2 seconds.
DNS request timed out.
    timeout was 2 seconds.
DNS request timed out.
    timeout was 2 seconds.
DNS request timed out.
    timeout was 2 seconds.
*** Не найден адрес для сервера ns1.urfu.ru: Timed out
> lserver ns1.urfu.ru
╤хЁтхЁ яю єьюыўрэш■:  ns1.urfu.ru
Address:  212.193.66.21
```

Почему так? Мы пытаемся получить ip у текущего несуществующего сервера (194.226.235.1) 

Команду server *name* мы используем, если хотим разрешать доменные имена с указанного сервера *name*, т.е он становится *default* server для текущего сенса nslookup. Если по какой-то причине этот сервер не отвечает на запросы, то и сменить сервер на другой мы не сможем (только, если не будем указывать ip). А с помощью команды lserver *name* это становится возможным, потому что имя другого сервера будет разрешено с нашего DNS-сервера, который стоит по умолчанию.

Воспользовались командой root:

```
> root
╤хЁтхЁ яю єьюыўрэш■:  A.ROOT-SERVERS.NET
Addresses:  2001:503:ba3e::2:30
          198.41.0.4
```

**5. Перейти в режим запроса записей NS (set q=ns или set type=ns), выяснить адреса серверов имён для доменов верхнего уровня (и их общее количество):**

```
> com.
╤хЁтхЁ:  A.ROOT-SERVERS.NET
Addresses:  2001:503:ba3e::2:30
          198.41.0.4

com     nameserver = a.gtld-servers.net
com     nameserver = b.gtld-servers.net
com     nameserver = c.gtld-servers.net
com     nameserver = d.gtld-servers.net
com     nameserver = e.gtld-servers.net
com     nameserver = f.gtld-servers.net
com     nameserver = g.gtld-servers.net
com     nameserver = h.gtld-servers.net
com     nameserver = i.gtld-servers.net
com     nameserver = j.gtld-servers.net
com     nameserver = k.gtld-servers.net
com     nameserver = l.gtld-servers.net
com     nameserver = m.gtld-servers.net
a.gtld-servers.net      internet address = 192.5.6.30
b.gtld-servers.net      internet address = 192.33.14.30
c.gtld-servers.net      internet address = 192.26.92.30
d.gtld-servers.net      internet address = 192.31.80.30
e.gtld-servers.net      internet address = 192.12.94.30
f.gtld-servers.net      internet address = 192.35.51.30
g.gtld-servers.net      internet address = 192.42.93.30
h.gtld-servers.net      internet address = 192.54.112.30
i.gtld-servers.net      internet address = 192.43.172.30
j.gtld-servers.net      internet address = 192.48.79.30
k.gtld-servers.net      internet address = 192.52.178.30
l.gtld-servers.net      internet address = 192.41.162.30
m.gtld-servers.net      internet address = 192.55.83.30
a.gtld-servers.net      AAAA IPv6 address = 2001:503:a83e::2:30
b.gtld-servers.net      AAAA IPv6 address = 2001:503:231d::2:30
```

```
> org.
╤хЁтхЁ:  A.ROOT-SERVERS.NET
Addresses:  2001:503:ba3e::2:30
          198.41.0.4

org     nameserver = d0.org.afilias-nst.org
org     nameserver = a0.org.afilias-nst.info
org     nameserver = c0.org.afilias-nst.info
org     nameserver = a2.org.afilias-nst.info
org     nameserver = b0.org.afilias-nst.org
org     nameserver = b2.org.afilias-nst.org
d0.org.afilias-nst.org  internet address = 199.19.57.1
d0.org.afilias-nst.org  AAAA IPv6 address = 2001:500:f::1
a0.org.afilias-nst.info internet address = 199.19.56.1
a0.org.afilias-nst.info AAAA IPv6 address = 2001:500:e::1
c0.org.afilias-nst.info internet address = 199.19.53.1
c0.org.afilias-nst.info AAAA IPv6 address = 2001:500:b::1
a2.org.afilias-nst.info internet address = 199.249.112.1
a2.org.afilias-nst.info AAAA IPv6 address = 2001:500:40::1
b0.org.afilias-nst.org  internet address = 199.19.54.1
b0.org.afilias-nst.org  AAAA IPv6 address = 2001:500:c::1
b2.org.afilias-nst.org  internet address = 199.249.120.1
b2.org.afilias-nst.org  AAAA IPv6 address = 2001:500:48::1
```

```
> ru.
╤хЁтхЁ:  A.ROOT-SERVERS.NET
Addresses:  2001:503:ba3e::2:30
          198.41.0.4

ru      nameserver = a.dns.ripn.net
ru      nameserver = b.dns.ripn.net
ru      nameserver = d.dns.ripn.net
ru      nameserver = e.dns.ripn.net
ru      nameserver = f.dns.ripn.net
a.dns.ripn.net  internet address = 193.232.128.6
b.dns.ripn.net  internet address = 194.85.252.62
d.dns.ripn.net  internet address = 194.190.124.17
e.dns.ripn.net  internet address = 193.232.142.17
f.dns.ripn.net  internet address = 193.232.156.17
a.dns.ripn.net  AAAA IPv6 address = 2001:678:17:0:193:232:128:6
b.dns.ripn.net  AAAA IPv6 address = 2001:678:16:0:194:85:252:62
d.dns.ripn.net  AAAA IPv6 address = 2001:678:18:0:194:190:124:17
e.dns.ripn.net  AAAA IPv6 address = 2001:678:15:0:193:232:142:17
f.dns.ripn.net  AAAA IPv6 address = 2001:678:14:0:193:232:156:17
```

**6. Пройти по цепочке серверов имён от корня и, по необходимости меняя в запросе тип записей (set q=…), найти ip-адрес для символьного имени и записать промежуточные данные в виде цепочки результатов запросов**

-

**7. Изучить способы получения с сервера всех записей (команда ls). Подключиться к нужному серверу, вывести на экран и сохранить в файл записи для:**

**Troubles, example:**

**Can't list domain edu.ru.: Server failed DNS-сервер отклонил передачу зоны edu.ru. на данный компьютер. Если это ошибка, проверьте параметры безопасности передачи зоны для edu.ru.*

**8. Получить «начальную запись зоны» (SOA – start of authority), выяснить вероятную дату последнего обновления зоны, время жизни записей в промежуточных кеширующих серверах и прочую информацию для:**

```
> ya.ru.
╤хЁтхЁ:  [8.8.8.8]
Address:  8.8.8.8

Не заслуживающий доверия ответ:
ya.ru
        primary name server = ns1.yandex.ru
        responsible mail addr = sysadmin.yandex.ru
        serial  = 2018031600
        refresh = 900 (15 mins)
        retry   = 600 (10 mins)
        expire  = 2592000 (30 days)
        default TTL = 900 (15 mins)
```

```
> mail.ru.
╤хЁтхЁ:  [8.8.8.8]
Address:  8.8.8.8

Не заслуживающий доверия ответ:
mail.ru
        primary name server = ns1.mail.ru
        responsible mail addr = hostmaster.mail.ru
        serial  = 3312752717
        refresh = 900 (15 mins)
        retry   = 900 (15 mins)
        expire  = 604800 (7 days)
        default TTL = 60 (1 min)
```

```
> urfu.ru.
╤хЁтхЁ:  [8.8.8.8]
Address:  8.8.8.8

Не заслуживающий доверия ответ:
urfu.ru
        primary name server = ns1.urfu.ru
        responsible mail addr = hostmaster.urfu.ru
        serial  = 2012091861
        refresh = 3600 (1 hour)
        retry   = 1800 (30 mins)
        expire  = 2419200 (28 days)
        default TTL = 3600 (1 hour)
```

**9. Найти на [www.iana.org](www.iana.org) [www.icann.org](www.icann.org) полный список доменов верхнего уровня. Выяснить на [www.nic.ru](www.nic.ru) стоимость регистрации собственного домена в различных зонах, необходимые для этого документы и способы оплаты. Найти (например, в google) регистратора с минимальной стоимостью домена в зоне ru. Найти регистратора с минимальной стоимость домена в зонах com и org**

