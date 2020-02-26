from os import path
import nonebot
import config

def main():
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__),'awesome','plugins')
        ,'awesome.plugins')
    nonebot.run()


if __name__ == '__main__':
    main()
