The following command enables to read packets from a pcap file and than write them back to a network interface:

`$RTE_TARGET/app/testpmd -c '0xf' -n 4 --vdev 'eth_pcap0,rx_pcap=/path/to/ file_rx.pcap,tx_iface=eth1' -- --port-topology=chained`

