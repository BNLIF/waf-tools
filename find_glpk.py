import os.path as osp
from waflib.Configure import conf


def options(opt):
    opt = opt.add_option_group('GLPK Options')
    opt.add_option('--with-glpk', type='string',
                   help="give GLPK installation location")
    opt.add_option('--with-glpk-include', type='string', default='',
                   help="give GLPK include installation location")
    opt.add_option('--with-glpk-lib', type='string', default='',
                   help="give GLPK lib installation location")


@conf
def check_glpk(ctx, mandatory=False):
    instdir = ctx.options.with_glpk

    if instdir is None or instdir.lower() in ['yes', 'true', 'on']:
        ctx.start_msg('Checking for GLPK in PKG_CONFIG_PATH')
        ctx.check_cfg(package='glpk',  uselib_store='GLPK',
                      args='--cflags --libs', mandatory=mandatory)
    elif instdir.lower() in ['no', 'off', 'false']:
        return
    else:
        ctx.start_msg('Checking for GLPK in %s' % instdir)
        if ctx.options.with_glpk_include:
            ctx.env.INCLUDES_GLPK = [ctx.options.with_glpk_include]
        else:
            ctx.env.INCLUDES_GLPK = [osp.join(instdir, 'include')]
        if ctx.options.with_glpk_lib:
            ctx.env.LIBPATH_GLPK = [ctx.options.with_glpk_lib]

    ctx.check(header_name="glpk.h", use='GLPK', mandatory=mandatory)
    # need to explicitly add floating point version of lib
    ctx.env.LIB_GLPK += ['glpk']
    # ibid if using double-precision:
    #ctx.env.LIB_FFTW += ['fftw3']
    if len(ctx.env.INCLUDES_GLPK):
        ctx.end_msg(ctx.env.INCLUDES_GLPK[0])
    else:
        ctx.end_msg('GLPK not found')


def configure(cfg):
    cfg.check_glpk()
