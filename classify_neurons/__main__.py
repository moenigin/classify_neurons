from gooey import Gooey, GooeyParser
from pathlib import Path

from .classify_neurons import ClassifyNeuronsViewer
from .utils import str2bool, parse_chg_stack


def run_classifier(args):
    """"""
    src = 'brainmaps://'
    raw_data = src + args.raw_data
    seg_layer = src + args.base_volume
    if args.change_stack_id:
        seg_layer = seg_layer + ':' + args.change_stack_id
    layers = {'segmentation': seg_layer}
    with ClassifyNeuronsViewer(targ_dir=args.targ_dir,
                               raw_data=raw_data,
                               layers=layers,
                               remove_token=args.remove_token,
                               timer_interval=args.timer_interval) as cls_neuron:
        cls_neuron.exit_event.wait()


@Gooey(program_name='classify_neurons', show_success_modal=False, image_dir=Path(__file__).resolve().parent.parent)
def main():
    """"""
    ap = GooeyParser()

    ap.add_argument("-targ_dir",
                    default=r'C:\Data\EM\classification',
                    type=str,
                    help="path to directory for saving proofreading data",
                    widget='DirChooser')

    ap.add_argument('-base_volume',
                    type=str,
                    default='487208920048:adultob:seg_v2_9nm_484558417fb_18nm_fb_107004781_otfa_multires_mesh',
                    help='base segmentation volume id in form of '
                         '"projectId:datasetId:volumeId"')

    ap.add_argument('-raw_data',
                    type=str,
                    default='487208920048:adultob:full',
                    help='image data volume path')

    ap.add_argument('-change_stack_id',
                    type=parse_chg_stack,
                    default='200614_prj487208920048_graph_postapr',
                    help='change stack id storing the agglomeration; to use '
                         'base volume enter one of: n, none, f. false, 0'
                         'graph')

    ap.add_argument('-remove_token',
                    type=str2bool,
                    default=False,
                    help='flag that decides whether to delete the token created'
                         ' by authenticating to neuroglancer upon exit of the '
                         'program. \n'
                         'Usage: true, yes, t, y, 1 or false, no, n, f, 0; '
                         'case-insensitive')

    ap.add_argument('-timer_interval',
                    type=int,
                    default=600,
                    help='interval of the autosave tiner in sec')

    ap.set_defaults(func=run_classifier)

    ap_args = ap.parse_args()

    ap_args.func(ap_args)
