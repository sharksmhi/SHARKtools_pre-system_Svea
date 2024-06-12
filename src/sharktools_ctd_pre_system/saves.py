
import yaml
from yaml.loader import SafeLoader
import pathlib
import json


def get_default_users():
    users = []
    for path in pathlib.Path(pathlib.Path(__file__).parent, 'defaults').iterdir():
        if path.suffix != '.yaml':
            continue
        users.append(path.stem)
    return sorted(users)


def get_default_user_file_path(user):
    users = get_default_users()
    if user not in users:
        return False
    return pathlib.Path(pathlib.Path(__file__).parent, 'defaults', f'{user}.yaml')


class Defaults:

    def __init__(self, user=None):
        self._this_directory = pathlib.Path(__file__).parent
        self._default_user_path = pathlib.Path(self._this_directory, 'default.user')

        self.file_path = None

        user = user or self.user
        # if not user:
        #     user = self._load_default_user()
        # if not user:
        #     user = 'default'

        self.file_path = get_default_user_file_path(user)
        if not self.file_path:
            raise Exception('Invalid user default path')
        self._save_default_user(user)

        self.data = {}

        self._load()

    def _load(self):
        """
        Loads dict from json
        :return:
        """
        if self.file_path and self.file_path.exists():
            with open(self.file_path) as fid:
                self.data = yaml.load(fid, Loader=SafeLoader)

    @property
    def user(self):
        return self._load_default_user() or 'default'

    def get(self, key, default=None):
        return self.data.get(key, default)

    def _save_default_user(self, user):
        if not user:
            return
        with open(self._default_user_path, 'w') as fid:
            fid.write(user)

    def _load_default_user(self):
        if not self._default_user_path.exists():
            return
        with open(self._default_user_path) as fid:
            return fid.read().strip()


class Saves:

    def __init__(self):
        self.file_path = pathlib.Path.home() / 'sharktools' / 'sharktools_ctd_pre_system.json'
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        self.data = {}

        self._load()

    def _load(self):
        """
        Loads dict from json
        :return:
        """
        if self.file_path.exists():
            with open(self.file_path) as fid:
                self.data = json.load(fid)

    def _save(self):
        """
        Writes information to json file.
        :return:
        """
        with open(self.file_path, 'w') as fid:
            json.dump(self.data, fid, indent=4, sort_keys=True)

    def set(self, key, value):
        if isinstance(value, pathlib.Path):
            value = str(value)
        elif isinstance(value, dict):
            new_value = {}
            for k, v in value.items():
                if isinstance(v, pathlib.Path):
                    v = str(v)
                new_value[k] = v
            value = new_value
        print(f'{type(value)=}: {value=}')
        self.data[key] = value
        self._save()

    def get(self, key, default=''):
        return self.data.get(key, default)


class SaveSelection:
    _saves = Saves()
    _defaults = Defaults()
    _saves_id_key = ''
    _selections_to_store = []

    def save_selection(self):
        data = {}
        if type(self._selections_to_store) == dict:
            for name, comp in self._selections_to_store.items():
                try:
                    data[name] = comp.get()
                except:
                    pass
        else:
            for comp in self._selections_to_store:
                try:
                    data[comp] = getattr(self, comp).get()
                except:
                    pass
        self._saves.set(self._saves_id_key, data)

    def load_selection(self, default_user=None, **kwargs):
        data = self._saves.get(self._saves_id_key)
        if not data:
            return
        if default_user:
            self._defaults = Defaults(user=default_user)
        if type(self._selections_to_store) == dict:
            for name, comp in self._selections_to_store.items():
                try:
                    value = self._defaults.get(name)
                    if value is None:
                        value = data.get(name, None)
                        if value is None:
                            continue
                    comp.set(value)
                except:
                    pass
        else:
            for comp in self._selections_to_store:
                try:
                    value = self._defaults.get(self._saves_id_key)
                    if value is None:
                        value = data.get(comp, None)
                        if value is None:
                            continue
                    getattr(self, comp).set(value)
                except:
                    raise


class SaveComponents:

    def __init__(self, key):
        self._saves = Saves()
        self._defaults = Defaults()
        self._saves_id_key = key
        self._components_to_store = set()

    def add_components(self, *args):
        for comp in args:
            self._components_to_store.add(comp)

    def save(self):
        data = {}
        for comp in self._components_to_store:
            try:
                data[comp._id] = str(comp.get())
                # print(f'SAVING: {comp._id} - {data[comp._id]}')
            except:
                pass
        self._saves.set(self._saves_id_key, data)

    def load(self):
        data = self._saves.get(self._saves_id_key)
        for comp in self._components_to_store:
            try:
                item = self._defaults.get(comp._id, None)
                if item is None:
                    item = data.get(comp._id, None)
                if item is None:
                    continue
                comp.set(item)
            except:
                pass

