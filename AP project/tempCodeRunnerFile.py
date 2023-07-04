system5 = Main()
        shared_ls = []
        def f0(shared_ls):
            shared_ls[0]=system1.main(search_word = "category-mobile-phone/product-list")
        def f1(shared_ls):
            shared_ls[1]=system2.main(search_word = "category-headphone")
        def f2(shared_ls):
            shared_ls[2]=system3.main(search_word = "category-tv2")
        def f3(shared_ls):
            shared_ls[3]=system4.main(search_word = "category-tablet")
        def f4(shared_ls):
            shared_ls[4]=system5.main(search_word = "notebook-netbook-ultrabook")
        
        t0 = Thread(target=lambda: f0(shared_ls))
        t1 = Thread(target=lambda: f1(shared_ls))
        t2 = Thread(target=lambda: f2(shared_ls))
        t3 = Thread(target=lambda: f3(shared_ls))
        t4 = Thread(target=lambda: f4(shared_ls))
        t0.start()
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t0.join()
        t1.join()
        t2.join()
        t3.join()
        t4.join()