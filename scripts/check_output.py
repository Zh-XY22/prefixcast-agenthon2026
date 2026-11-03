"""Official gates-only check; never creates predictions or performance scores."""
import argparse,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'runtime/official'))
from qfbench2_track_forecasting.scoring import _cmd_score
p=argparse.ArgumentParser();p.add_argument('--card',required=True);p.add_argument('--forecast',required=True);a=p.parse_args()
raise SystemExit(_cmd_score(argparse.Namespace(card=a.card,forecast=a.forecast,realized=None)))
