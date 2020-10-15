import sys

from copy import deepcopy
from pathlib import Path

from agglomeration_proofreading.viewer_bases import _ViewerBase
from .utils import load_file, file_pattern, write_json, mk_time_stamp_str


# todo:
#  - autosave from neuroproofreader
#  - script that checks for chrome version installed in the default location
#  and downloads the respective chrome driver to be unpacked and referenced to
#  in a temporary dir. If the chrome version is not found, downloads the latest
#  version of chrome driver available. If this does not work return error. This
#  would be best implemented as a separate class, maybe even function for the
#  agglomeration proofreading viewer_bases


class ClassifyNeuronsViewer(_ViewerBase):
    """"""

    def __init__(self, targ_dir, raw_data, layers, remove_token, timer_interval):

        super(ClassifyNeuronsViewer, self).__init__(raw_data=raw_data,
                                                    layers=layers,
                                                    remove_token=remove_token,
                                                    timer_interval=timer_interval)
        if timer_interval is not None:
            self.timer.start_timer(func=self.save_file)
        self.targ_dir = targ_dir
        self.layer_name = list(layers.keys())[0]
        try:
            self.data = load_file(targ_dir)
        except FileNotFoundError:
            msg = 'Could not find an appropriate src file in' + str(targ_dir)
            self.upd_msg(msg)
            return

        # load first neuron and register
        if list(self.data.keys()) == [-1]:
            self.current_idx = -1
            self.current_neuron = None
            self.current_group = None
            self.next_neuron()
            self.to_group('new')
        else:
            self.current_idx = 0
            self.current_group = self.max_group_id()
            self.display_current()

    def _set_keybindings(self):
        """"""
        super()._set_keybindings()
        self.viewer.actions.add('next_neuron',
                                lambda s: self.next_neuron())
        self.viewer.actions.add('previous_neuron',
                                lambda s: self.prev_neuron())
        self.viewer.actions.add('neuron_to_current_group',
                                lambda s: self.to_group())
        self.viewer.actions.add('neuron_to_new_group',
                                lambda s: self.to_group('new'))
        self.viewer.actions.add('next_group',
                                lambda s: self.next_group())
        self.viewer.actions.add('previous_group',
                                lambda s: self.prev_group())
        self.viewer.actions.add('remove_neuron_from_group',
                                lambda s: self.remove_from_group())
        self.viewer.actions.add('toogle_group_display',
                                lambda s: self.toogle_group())
        self.viewer.actions.add('selected_neurons_to_group',
                                lambda s: self.selected_to_group())
        self.viewer.actions.add('save',
                                lambda s: self.save_file())
        self.viewer.actions.add('exit',
                                lambda s: self.exit())
        if getattr(sys, 'freeze', False):
            # running as bundle (aka frozen)
            _DEFAULT_DIR = sys._MEIPASS
        else:
            _DEFAULT_DIR = Path(__file__).resolve().parent

        fn = 'KEYBINDINGS_neuronclassifier.ini'
        ini_file = Path(_DEFAULT_DIR).joinpath(fn)
        if not Path(ini_file).exists():
            raise FileNotFoundError

        self._bind_pairs(ini_file)

    def next_neuron(self):
        """increments neuron index and triggers viewer update"""
        if self.current_idx + 1 == len(self.data[-1]):
            self.current_idx = 0
        else:
            self.current_idx += 1

        self.display_current()

    def prev_neuron(self):
        """decrements neuron index and triggers viewer update"""
        if self.current_idx == 0:
            self.current_idx = len(self.data[-1]) - 1
        else:
            self.current_idx -= 1

        self.display_current()

    def display_current(self):
        """triggers display of current neuron and neuron group in the viewer"""
        self.current_neuron = self.data[-1][self.current_idx]
        group = []
        if self.current_group is not None:
            group = deepcopy(self.data[self.current_group])
        group.append(self.current_neuron)
        self.upd_viewer_segments(self.layer_name, group)
        self.display_info()

    def display_info(self):
        """displays current group and neuron idx in the neuroglancer message
        panel"""
        msg = 'current neuron {}, active group {}'.format(self.current_neuron,
                                                          self.current_group)
        self.upd_msg(msg)

    def max_group_id(self):
        """return maximal neuron group id larger than -1"""
        return max([x for x in self.data.keys() if x != -1])

    def to_group(self, mode=None):
        """assigns the current neuron to a group

        Args:
            mode(str, optional): if mode is new a new group is opened and the
                                 current neuron assigned to it

        """

        if mode == 'new':
            if self.current_group is not None:
                self.current_group = self.max_group_id() + 1
            else:
                self.current_group = 0

        if self.current_group not in self.data.keys():
            self.data[self.current_group] = []

        self.data[self.current_group].append(self.current_neuron)
        self.data[-1].remove(self.current_neuron)
        msg = 'neuron {} was assigned to group {}'.format(self.current_neuron,
                                                          self.current_group)
        self.upd_msg(msg)
        self.next_neuron()

    def next_group(self):
        """displays next neuron group"""
        self.current_group += 1
        if self.current_group > self.max_group_id():
            self.current_group = 0

        self.display_current()

    def prev_group(self):
        """displays previous neuron group"""
        if self.current_group is None:
            msg = 'no groups defined yet'
            self.upd_msg(msg)
            return
        self.current_group -= 1
        if self.current_group == -1:
            self.current_group = self.max_group_id()

        self.display_current()

    def remove_from_group(self):
        """removes the neuron in the viewer from the group it was assigned to"""
        viewer_segments = list(
            self.viewer.state.layers[self.layer_name].segments)
        if len(viewer_segments) != 1:
            msg = 'A single segment has to be in the viewer in order to remove ' \
                  'it from the group it has been assigned to'
            self.upd_msg(msg)
            return

        segment = int(viewer_segments[0])

        for k, v in self.data.items():
            if segment in v:
                group_id = k
                break

        if group_id == -1:
            msg = 'the neuron in the viewer has not been assigned to any group yet'
            self.upd_msg(msg)
            return

        try:
            self.data[group_id].remove(segment)
            self.data[-1].append(segment)
        except Exception as e:
            msg = 'could not remove neuron {} from group {}'.format(segment,
                                                                    self.current_group)
            self.upd_msg(msg)
            print('removal of segment', segment, 'from group', self.group,
                  'failed with error', e, flush=True)

    def selected_to_group(self):
        """Assigns the segments visible in the viewer to a new group"""
        viewer_segments = [int(seg) for seg in
                           self.viewer.state.layers[self.layer_name].segments]
        msg = 'Neurons in viewer will be assigned to a new group'
        self.upd_msg(msg)

        # remove the segments from the groups they are currently assigned to
        for seg in viewer_segments:
            key = [k for k, v in self.data.items() if seg in v]
            if len(key) > 1:
                raise ValueError(' this should not happen, neuron ', seg,
                                 'assigned to 2 groups ')
            key = key[0]
            self.data[key].remove(seg)

        # assign neurons in viewer to new group
        new_id = self.max_group_id()+1
        self.data[new_id] = viewer_segments

        msg = 'Neurons in viewer were assigned to group' + str(new_id)
        self.upd_msg(msg)

        self.current_group = new_id
        self.next_neuron()

    def toogle_group(self):
        """toggles visibility of the neurons in the current group"""
        viewer_segments = list(
            self.viewer.state.layers[self.layer_name].segments)
        if len(viewer_segments) == 1:
            self.display_current()
        else:
            self.upd_viewer_segments(self.layer_name, self.current_neuron)

    def exit(self):
        """saves data and exits program"""
        self.save_file()
        self.exit_event.set()

    def save_file(self):
        """"""
        fn = Path(self.targ_dir).joinpath(mk_time_stamp_str() + file_pattern)
        write_json(self.data, fn)
