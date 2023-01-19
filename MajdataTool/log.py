class Log:
    isDebug = False

    # show debug log or not, don't display by default
    @classmethod
    def Set_Debug_Mod(cls, bl):
        cls.isDebug = bl
        return

    # show debug message
    @classmethod
    def Message(cls, msg):
        if cls.isDebug:
            print(msg)
        return
