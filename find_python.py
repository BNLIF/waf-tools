import os.path as osp
import sys
from waflib.Configure import conf


def options(opt):
    opt = opt.add_option_group('python Options')
    opt.add_option('--with-python', type='string',
                   help="give python installation location")
    opt.add_option('--with-python-include', type='string', default='',
                   help="give python include installation location")
    opt.add_option('--with-python-lib', type='string', default='',
                   help="give python lib installation location")


@conf
def check_python(ctx, mandatory=True):
    instdir = ctx.options.with_python

    if instdir is None or instdir.lower() in ['yes', 'true', 'on']:
        ctx.start_msg('Checking for PYTHON in PKG_CONFIG_PATH')
        ctx.check_cfg(package='python',  uselib_store='PYTHON',
                      args='--cflags --libs', mandatory=mandatory)
    elif instdir.lower() in ['no', 'off', 'false']:
        return
    else:
        ctx.start_msg('Checking for PYTHON in %s' % instdir)
        if ctx.options.with_python_include:
            ctx.env.INCLUDES_PYTHON = [ctx.options.with_python_include]
        else:
            ctx.env.INCLUDES_PYTHON = [osp.join(instdir, 'include')]
        if ctx.options.with_python_lib:
            ctx.env.LIBPATH_PYTHON = [ctx.options.with_python_lib]

    ctx.check(header_name="Python.h", use='PYTHON', mandatory=mandatory)
    # need to explicitly add floating point version of lib
    python_lib = 'python{}.{}'.format(sys.version_info[:][0],sys.version_info[:][1])
    #print('python lib: "{}"'.format(python_lib))
    ctx.env.LIB_PYTHON += [python_lib, 'pthread', 'dl', 'util', 'm']
    if len(ctx.env.INCLUDES_PYTHON):
        ctx.end_msg(ctx.env.INCLUDES_PYTHON[0])
    else:
        ctx.end_msg('PYTHON not found')


def configure(cfg):
    cfg.check_python()
