class cla:
    def cc(self):
        print(":CC---------")

class clb(cla):
    def cc(self):
        super().cc()
        print("fiudfghdghwriufg suyhgsugsg hisdfi erhitigh tgiti gh")


a = clb()
a.cc()