import sys
import subprocess
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline

        sys.stderr.write("looking for kube context\n")
        try:
            context = subprocess.check_output(['kubectl', 'config',
                                               'current-context']).strip()
        except subprocess.CalledProcessError:
            # CalledProcessError is thrown if non-zero returncode, like if we
            # don't have a kubectl context
            return

        # Any kubectl context that isn't marked as safe in your segment config
        # is considered as "production", which you should really be cognizant
        # of. Can be a bit obnoxious when you always work in prod, but aeh.
        # I keep config in ~/.powerline-shell.json for convenience.
        safe_contexts = powerline.segment_conf("kubectl_context", "safe_contexts")
        powerline.append(' %s ' % context,
                         powerline.theme.VIRTUAL_ENV_FG,
                         powerline.theme.VIRTUAL_ENV_BG if context in safe_contexts else 161)
