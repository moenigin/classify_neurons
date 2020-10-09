from gooey import Gooey, GooeyParser

from .classify_neurons import ClassifyNeuronsViewer
from .utils import str2bool


def run_classifier(args):
    """"""
    src = 'brainmaps://'
    raw_data = src + args.raw_data
    seg_layer = src + args.base_volume + ':' + args.change_stack_id
    layers = {'segmentation': seg_layer}
    with ClassifyNeuronsViewer(targ_dir=args.targ_dir,
                               raw_data=raw_data,
                               layers=layers,
                               remove_token=args.remove_token) as cls_neuron:
        cls_neuron.exit_event.wait()


@Gooey
def main():
    """"""
    ap = GooeyParser()

    ap.add_argument("-targ_dir",
                    default=r'C:\Data\EM\test',
                    type=str,
                    help="path to directory for saving proofreading data",
                    widget='FileChooser')

    ap.add_argument('-base_volume',
                    type=str,
                    default='487208920048:adultob:seg_v2_9nm_484558417fb_18nm_fb_107004781_otfa',
                    help='base segmentation volume id in form of '
                         '"projectId:datasetId:volumeId"')

    ap.add_argument('-raw_data',
                    type=str,
                    default='487208920048:adultob:full',
                    help='image data volume path')

    ap.add_argument('-change_stack_id',
                    type=str,
                    default='200614_prj487208920048_graph_postapr',
                    help='id of the change stack storing the agglomeration '
                         'graph')

    ap.add_argument('-remove_token',
                    type=str2bool,
                    default=False,
                    help='flag that decides whether to delete the token created'
                         ' by authenticating to neuroglancer upon exit of the '
                         'program. \n'
                         'Usage: true, yes, t, y, 1 or false, no, n, f, 0; '
                         'case-insensitive')

    ap.set_defaults(func=run_classifier)

    ap_args = ap.parse_args()

    ap_args.func(ap_args)

