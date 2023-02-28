from asyncio import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import subprocess
from os import environ

class Browser_Runner(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, RunCommand())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):

        arg = event.get_argument()
    
        if arg == None: 
            arg = ""


        data = { "arg": arg }

        return RenderResultListAction([ExtensionResultItem(icon="images/icon.png",
                                                           name="Search %s" %arg,
                                                           on_enter=ExtensionCustomAction(data))])


class RunCommand(EventListener):

    def on_event(self, event, extension):

        data = event.get_data()
        
        browser = extension.preferences["br"]
        engine = extension.preferences["ng"]
        arg = data["arg"]

        if engine != None:
            if arg[:2] != ">>":
                tmp = arg
                tmp = tmp.replace("+","%2B")
                tmp = tmp.replace(" ","+")
                arg = engine+tmp
            else:
                arg = arg[2:]

        subprocess.run( [f'{browser} "{arg}"'], shell=True )

        return HideWindowAction()



if __name__ == '__main__':
    Browser_Runner().run()