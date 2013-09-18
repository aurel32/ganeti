#
#

# Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013 Google Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.


"""Module holding different constants."""

import re
import socket

from ganeti import _autoconf
from ganeti import _constants
from ganeti import _vcsversion
from ganeti import compat
from ganeti import pathutils


# various versions
RELEASE_VERSION = _autoconf.PACKAGE_VERSION
OS_API_V10 = 10
OS_API_V15 = 15
OS_API_V20 = 20
OS_API_VERSIONS = compat.UniqueFrozenset([
  OS_API_V10,
  OS_API_V15,
  OS_API_V20,
  ])
VCS_VERSION = _vcsversion.VCS_VERSION
EXPORT_VERSION = 0
RAPI_VERSION = 2


# Format for CONFIG_VERSION:
#   01 03 0123 = 01030123
#   ^^ ^^ ^^^^
#   |  |  + Configuration version/revision
#   |  + Minor version
#   + Major version
#
# It is stored as an integer. Make sure not to write an octal number.

# BuildVersion and SplitVersion must be in here because we can't import other
# modules. The cfgupgrade tool must be able to read and write version numbers
# and thus requires these functions. To avoid code duplication, they're kept in
# here.

def BuildVersion(major, minor, revision):
  """Calculates int version number from major, minor and revision numbers.

  Returns: int representing version number

  """
  assert isinstance(major, int)
  assert isinstance(minor, int)
  assert isinstance(revision, int)
  return (1000000 * major +
            10000 * minor +
                1 * revision)


def SplitVersion(version):
  """Splits version number stored in an int.

  Returns: tuple; (major, minor, revision)

  """
  assert isinstance(version, int)

  (major, remainder) = divmod(version, 1000000)
  (minor, revision) = divmod(remainder, 10000)

  return (major, minor, revision)


CONFIG_MAJOR = int(_autoconf.VERSION_MAJOR)
CONFIG_MINOR = int(_autoconf.VERSION_MINOR)
CONFIG_REVISION = 0
CONFIG_VERSION = BuildVersion(CONFIG_MAJOR, CONFIG_MINOR, CONFIG_REVISION)

#: RPC protocol version
PROTOCOL_VERSION = BuildVersion(CONFIG_MAJOR, CONFIG_MINOR, 0)

# user separation
DAEMONS_GROUP = _constants.DAEMONS_GROUP
ADMIN_GROUP = _constants.ADMIN_GROUP
MASTERD_USER = _constants.MASTERD_USER
MASTERD_GROUP = _constants.MASTERD_GROUP
RAPI_USER = _constants.RAPI_USER
RAPI_GROUP = _constants.RAPI_GROUP
CONFD_USER = _constants.CONFD_USER
CONFD_GROUP = _constants.CONFD_GROUP
LUXID_USER = _constants.LUXID_USER
LUXID_GROUP = _constants.LUXID_GROUP
NODED_USER = _constants.NODED_USER
NODED_GROUP = _constants.NODED_GROUP
MOND_USER = _constants.MOND_USER
MOND_GROUP = _constants.MOND_GROUP
SSH_LOGIN_USER = _constants.SSH_LOGIN_USER
SSH_CONSOLE_USER = _constants.SSH_CONSOLE_USER

# cpu pinning separators and constants
CPU_PINNING_SEP = ":"
CPU_PINNING_ALL = "all"
# internal representation of "all"
CPU_PINNING_ALL_VAL = -1
# one "all" entry in a CPU list means CPU pinning is off
CPU_PINNING_OFF = [CPU_PINNING_ALL_VAL]

# A Xen-specific implementation detail - there is no way to actually say
# "use any cpu for pinning" in a Xen configuration file, as opposed to the
# command line, where you can say "xm vcpu-pin <domain> <vcpu> all".
# The workaround used in Xen is "0-63" (see source code function
# xm_vcpu_pin in <xen-source>/tools/python/xen/xm/main.py).
# To support future changes, the following constant is treated as a
# blackbox string that simply means use-any-cpu-for-pinning-under-xen.
CPU_PINNING_ALL_XEN = "0-63"

# A KVM-specific implementation detail - the following value is used
# to set CPU affinity to all processors (#0 through #31), per taskset
# man page.
# FIXME: This only works for machines with up to 32 CPU cores
CPU_PINNING_ALL_KVM = 0xFFFFFFFF

# Wipe
DD_CMD = "dd"
MAX_WIPE_CHUNK = 1024 # 1GB
MIN_WIPE_CHUNK_PERCENT = 10

RUN_DIRS_MODE = 0775
SECURE_DIR_MODE = 0700
SECURE_FILE_MODE = 0600
ADOPTABLE_BLOCKDEV_ROOT = "/dev/disk/"
ENABLE_CONFD = _autoconf.ENABLE_CONFD
ENABLE_MOND = _autoconf.ENABLE_MOND
ENABLE_SPLIT_QUERY = _autoconf.ENABLE_SPLIT_QUERY
ENABLE_RESTRICTED_COMMANDS = _autoconf.ENABLE_RESTRICTED_COMMANDS

# SSH constants
SSH = _constants.SSH
SCP = _constants.SCP

NODED = _constants.NODED
CONFD = _constants.CONFD
LUXID = _constants.LUXID
RAPI = _constants.RAPI
MASTERD = _constants.MASTERD
MOND = _constants.MOND

DAEMONS = _constants.DAEMONS

DAEMONS_PORTS = _constants.DAEMONS_PORTS

DEFAULT_NODED_PORT = _constants.DEFAULT_NODED_PORT
DEFAULT_CONFD_PORT = _constants.DEFAULT_CONFD_PORT
DEFAULT_MOND_PORT = _constants.DEFAULT_MOND_PORT
DEFAULT_RAPI_PORT = _constants.DEFAULT_RAPI_PORT

FIRST_DRBD_PORT = 11000
LAST_DRBD_PORT = 14999

DAEMONS_LOGBASE = _constants.DAEMONS_LOGBASE

DAEMONS_LOGFILES = \
    dict((daemon, pathutils.GetLogFilename(DAEMONS_LOGBASE[daemon]))
         for daemon in DAEMONS_LOGBASE)

# Some daemons might require more than one logfile.
# Specifically, right now only the Haskell http library "snap", used by the
# monitoring daemon, requires multiple log files.

# These are the only valid reasons for having an extra logfile
EXTRA_LOGREASON_ACCESS = "access"
EXTRA_LOGREASON_ERROR = "error"

VALID_EXTRA_LOGREASONS = compat.UniqueFrozenset([
  EXTRA_LOGREASON_ACCESS,
  EXTRA_LOGREASON_ERROR,
  ])

# These are the extra logfiles, grouped by daemon
DAEMONS_EXTRA_LOGBASE = {
  MOND: {
    EXTRA_LOGREASON_ACCESS: _constants.EXTRA_LOGREASON_ACCESS,
    EXTRA_LOGREASON_ERROR: _constants.EXTRA_LOGREASON_ERROR,
    }
  }

DAEMONS_EXTRA_LOGFILES = \
  dict((daemon, dict((extra,
       pathutils.GetLogFilename(DAEMONS_EXTRA_LOGBASE[daemon][extra]))
       for extra in DAEMONS_EXTRA_LOGBASE[daemon]))
         for daemon in DAEMONS_EXTRA_LOGBASE)

DEV_CONSOLE = _constants.DEV_CONSOLE

PROC_MOUNTS = "/proc/mounts"

# Local UniX Interface related constants
LUXI_EOM = chr(3)
LUXI_VERSION = CONFIG_VERSION
#: Environment variable for the luxi override socket
LUXI_OVERRIDE = "FORCE_LUXI_SOCKET"
LUXI_OVERRIDE_MASTER = "master"
LUXI_OVERRIDE_QUERY = "query"

# one of "no", "yes", "only"
SYSLOG_USAGE = _constants.SYSLOG_USAGE
SYSLOG_NO = _constants.SYSLOG_NO
SYSLOG_YES = _constants.SYSLOG_YES
SYSLOG_ONLY = _constants.SYSLOG_ONLY
SYSLOG_SOCKET = _constants.SYSLOG_SOCKET

EXPORT_CONF_FILE = "config.ini"

XEN_BOOTLOADER = _constants.XEN_BOOTLOADER
XEN_KERNEL = _constants.XEN_KERNEL
XEN_INITRD = _constants.XEN_INITRD
XEN_CMD_XM = _constants.XEN_CMD_XM
XEN_CMD_XL = _constants.XEN_CMD_XL
KNOWN_XEN_COMMANDS = _constants.KNOWN_XEN_COMMANDS

# When the Xen toolstack used is "xl", live migration requires the source host
# to connect to the target host via ssh (xl runs this command). We need to pass
# the command xl runs some extra info so that it can use Ganeti's key
# verification and not fail. Note that this string is incomplete: it must be
# filled with the cluster name before being used.
XL_SSH_CMD = ("ssh -l %s -oGlobalKnownHostsFile=%s"
              " -oUserKnownHostsFile=/dev/null"
              " -oCheckHostIp=no -oStrictHostKeyChecking=yes"
              " -oHostKeyAlias=%%s") % (SSH_LOGIN_USER,
                                        pathutils.SSH_KNOWN_HOSTS_FILE)

KVM_PATH = _autoconf.KVM_PATH
KVM_KERNEL = _autoconf.KVM_KERNEL
SOCAT_PATH = _autoconf.SOCAT_PATH
SOCAT_USE_ESCAPE = _autoconf.SOCAT_USE_ESCAPE
SOCAT_USE_COMPRESS = _autoconf.SOCAT_USE_COMPRESS
SOCAT_ESCAPE_CODE = "0x1d"

#: Console as SSH command
CONS_SSH = "ssh"

#: Console as VNC server
CONS_VNC = "vnc"

#: Console as SPICE server
CONS_SPICE = "spice"

#: Display a message for console access
CONS_MESSAGE = "msg"

#: All console types
CONS_ALL = compat.UniqueFrozenset([
  CONS_SSH,
  CONS_VNC,
  CONS_SPICE,
  CONS_MESSAGE,
  ])

# For RSA keys more bits are better, but they also make operations more
# expensive. NIST SP 800-131 recommends a minimum of 2048 bits from the year
# 2010 on.
RSA_KEY_BITS = 2048

# Ciphers allowed for SSL connections. For the format, see ciphers(1). A better
# way to disable ciphers would be to use the exclamation mark (!), but socat
# versions below 1.5 can't parse exclamation marks in options properly. When
# modifying the ciphers, ensure not to accidentially add something after it's
# been removed. Use the "openssl" utility to check the allowed ciphers, e.g.
# "openssl ciphers -v HIGH:-DES".
OPENSSL_CIPHERS = "HIGH:-DES:-3DES:-EXPORT:-ADH"

# Digest used to sign certificates ("openssl x509" uses SHA1 by default)
X509_CERT_SIGN_DIGEST = "SHA1"

# Default validity of certificates in days
X509_CERT_DEFAULT_VALIDITY = 365 * 5

# commonName (CN) used in certificates
X509_CERT_CN = "ganeti.example.com"

X509_CERT_SIGNATURE_HEADER = "X-Ganeti-Signature"

# Import/export daemon mode
IEM_IMPORT = "import"
IEM_EXPORT = "export"

# Import/export transport compression
IEC_NONE = "none"
IEC_GZIP = "gzip"
IEC_ALL = compat.UniqueFrozenset([
  IEC_NONE,
  IEC_GZIP,
  ])

IE_CUSTOM_SIZE = "fd"

IE_MAGIC_RE = re.compile(r"^[-_.a-zA-Z0-9]{5,100}$")

# Import/export I/O
# Direct file I/O, equivalent to a shell's I/O redirection using '<' or '>'
IEIO_FILE = "file"
# Raw block device I/O using "dd"
IEIO_RAW_DISK = "raw"
# OS definition import/export script
IEIO_SCRIPT = "script"

VALUE_DEFAULT = "default"
VALUE_AUTO = "auto"
VALUE_GENERATE = "generate"
VALUE_NONE = "none"
VALUE_TRUE = "true"
VALUE_FALSE = "false"
VALUE_HS_NOTHING = {"Nothing": None}


# External script validation mask
EXT_PLUGIN_MASK = re.compile("^[a-zA-Z0-9_-]+$")

# hooks-related constants
HOOKS_PHASE_PRE = "pre"
HOOKS_PHASE_POST = "post"
HOOKS_NAME_CFGUPDATE = "config-update"
HOOKS_NAME_WATCHER = "watcher"
HOOKS_VERSION = 2
HOOKS_PATH = "/sbin:/bin:/usr/sbin:/usr/bin"

# hooks subject type (what object type does the LU deal with)
HTYPE_CLUSTER = "CLUSTER"
HTYPE_NODE = "NODE"
HTYPE_GROUP = "GROUP"
HTYPE_INSTANCE = "INSTANCE"
HTYPE_NETWORK = "NETWORK"

HKR_SKIP = 0
HKR_FAIL = 1
HKR_SUCCESS = 2

# Storage types
ST_BLOCK = _constants.ST_BLOCK
ST_DISKLESS = _constants.ST_DISKLESS
ST_EXT = _constants.ST_EXT
ST_FILE = _constants.ST_FILE
ST_LVM_PV = _constants.ST_LVM_PV
ST_LVM_VG = _constants.ST_LVM_VG
ST_RADOS = _constants.ST_RADOS
STORAGE_TYPES = _constants.STORAGE_TYPES

# the set of storage types for which storage reporting is available
# FIXME: Remove this, once storage reporting is available for all types.
STS_REPORT = compat.UniqueFrozenset([ST_FILE, ST_LVM_PV, ST_LVM_VG])

# Storage fields
# first two are valid in LU context only, not passed to backend
SF_NODE = _constants.SF_NODE
SF_TYPE = _constants.SF_TYPE
# and the rest are valid in backend
SF_NAME = _constants.SF_NAME
SF_SIZE = _constants.SF_SIZE
SF_FREE = _constants.SF_FREE
SF_USED = _constants.SF_USED
SF_ALLOCATABLE = _constants.SF_ALLOCATABLE

# Storage operations
SO_FIX_CONSISTENCY = "fix-consistency"

# Available fields per storage type
VALID_STORAGE_FIELDS = compat.UniqueFrozenset([
  SF_NODE,
  SF_NAME,
  SF_TYPE,
  SF_SIZE,
  SF_USED,
  SF_FREE,
  SF_ALLOCATABLE,
  ])

MODIFIABLE_STORAGE_FIELDS = {
  ST_LVM_PV: frozenset([SF_ALLOCATABLE]),
  }

VALID_STORAGE_OPERATIONS = {
  ST_LVM_VG: frozenset([SO_FIX_CONSISTENCY]),
  }

# Volume fields
VF_DEV = "dev"
VF_INSTANCE = "instance"
VF_NAME = "name"
VF_NODE = "node"
VF_PHYS = "phys"
VF_SIZE = "size"
VF_VG = "vg"

# Local disk status
# Note: Code depends on LDS_OKAY < LDS_UNKNOWN < LDS_FAULTY
(LDS_OKAY,
 LDS_UNKNOWN,
 LDS_FAULTY) = range(1, 4)

LDS_NAMES = {
  LDS_OKAY: "ok",
  LDS_UNKNOWN: "unknown",
  LDS_FAULTY: "faulty",
}

# disk template types
DT_BLOCK = _constants.DT_BLOCK
DT_DISKLESS = _constants.DT_DISKLESS
DT_DRBD8 = _constants.DT_DRBD8
DT_EXT = _constants.DT_EXT
DT_FILE = _constants.DT_FILE
DT_PLAIN = _constants.DT_PLAIN
DT_RBD = _constants.DT_RBD
DT_SHARED_FILE = _constants.DT_SHARED_FILE
DISK_TEMPLATE_PREFERENCE = _constants.DISK_TEMPLATE_PREFERENCE
DISK_TEMPLATES = _constants.DISK_TEMPLATES
DEFAULT_ENABLED_DISK_TEMPLATES = _constants.DEFAULT_ENABLED_DISK_TEMPLATES

# mapping of disk templates to storage types
MAP_DISK_TEMPLATE_STORAGE_TYPE = {
  DT_BLOCK: ST_BLOCK,
  DT_DISKLESS: ST_DISKLESS,
  DT_DRBD8: ST_LVM_VG,
  DT_EXT: ST_EXT,
  DT_FILE: ST_FILE,
  DT_PLAIN: ST_LVM_VG,
  DT_RBD: ST_RADOS,
  DT_SHARED_FILE: ST_FILE,
  }

# the set of network-mirrored disk templates
DTS_INT_MIRROR = compat.UniqueFrozenset([DT_DRBD8])

# the set of externally-mirrored disk templates (e.g. SAN, NAS)
DTS_EXT_MIRROR = compat.UniqueFrozenset([
  DT_DISKLESS, # 'trivially' externally mirrored
  DT_SHARED_FILE,
  DT_BLOCK,
  DT_RBD,
  DT_EXT,
  ])

# the set of non-lvm-based disk templates
DTS_NOT_LVM = compat.UniqueFrozenset([
  DT_DISKLESS,
  DT_FILE,
  DT_SHARED_FILE,
  DT_BLOCK,
  DT_RBD,
  DT_EXT,
  ])

# the set of disk templates which can be grown
DTS_GROWABLE = compat.UniqueFrozenset([
  DT_PLAIN,
  DT_DRBD8,
  DT_FILE,
  DT_SHARED_FILE,
  DT_RBD,
  DT_EXT,
  ])

# the set of disk templates that allow adoption
DTS_MAY_ADOPT = compat.UniqueFrozenset([
  DT_PLAIN,
  DT_BLOCK,
  ])

# the set of disk templates that *must* use adoption
DTS_MUST_ADOPT = compat.UniqueFrozenset([DT_BLOCK])

# the set of disk templates that allow migrations
DTS_MIRRORED = frozenset.union(DTS_INT_MIRROR, DTS_EXT_MIRROR)

# the set of file based disk templates
DTS_FILEBASED = compat.UniqueFrozenset([
  DT_FILE,
  DT_SHARED_FILE,
  ])

# the set of disk templates that can be moved by copying
# Note: a requirement is that they're not accessed externally or shared between
# nodes; in particular, sharedfile is not suitable.
DTS_COPYABLE = compat.UniqueFrozenset([
  DT_FILE,
  DT_PLAIN,
  ])

# the set of disk templates that are supported by exclusive_storage
DTS_EXCL_STORAGE = compat.UniqueFrozenset([DT_PLAIN])

# templates for which we don't perform checks on free space
DTS_NO_FREE_SPACE_CHECK = compat.UniqueFrozenset([
  DT_FILE,
  DT_SHARED_FILE,
  DT_RBD,
  DT_EXT,
  ])

DTS_BLOCK = compat.UniqueFrozenset([
  DT_PLAIN,
  DT_DRBD8,
  DT_BLOCK,
  DT_RBD,
  DT_EXT,
  ])

# drbd constants
DRBD_HMAC_ALG = "md5"
DRBD_DEFAULT_NET_PROTOCOL = "C"
DRBD_MIGRATION_NET_PROTOCOL = "C"
DRBD_STATUS_FILE = "/proc/drbd"

#: Size of DRBD meta block device
DRBD_META_SIZE = 128

# drbd barrier types
DRBD_B_NONE = "n"
DRBD_B_DISK_BARRIERS = "b"
DRBD_B_DISK_DRAIN = "d"
DRBD_B_DISK_FLUSH = "f"

# Valid barrier combinations: "n" or any non-null subset of "bfd"
DRBD_VALID_BARRIER_OPT = compat.UniqueFrozenset([
  frozenset([DRBD_B_NONE]),
  frozenset([DRBD_B_DISK_BARRIERS]),
  frozenset([DRBD_B_DISK_DRAIN]),
  frozenset([DRBD_B_DISK_FLUSH]),
  frozenset([DRBD_B_DISK_DRAIN, DRBD_B_DISK_FLUSH]),
  frozenset([DRBD_B_DISK_BARRIERS, DRBD_B_DISK_DRAIN]),
  frozenset([DRBD_B_DISK_BARRIERS, DRBD_B_DISK_FLUSH]),
  frozenset([DRBD_B_DISK_BARRIERS, DRBD_B_DISK_FLUSH, DRBD_B_DISK_DRAIN]),
  ])

# rbd tool command
RBD_CMD = "rbd"

# file backend driver
FD_BLKTAP = _constants.FD_BLKTAP
FD_LOOP = _constants.FD_LOOP

# the set of drbd-like disk types
LDS_DRBD = compat.UniqueFrozenset([DT_DRBD8])

# disk access mode
DISK_RDONLY = _constants.DISK_RDONLY
DISK_RDWR = _constants.DISK_RDWR
DISK_ACCESS_SET = _constants.DISK_ACCESS_SET

# disk replacement mode
REPLACE_DISK_PRI = "replace_on_primary"    # replace disks on primary
REPLACE_DISK_SEC = "replace_on_secondary"  # replace disks on secondary
REPLACE_DISK_CHG = "replace_new_secondary" # change secondary node
REPLACE_DISK_AUTO = "replace_auto"
REPLACE_MODES = compat.UniqueFrozenset([
  REPLACE_DISK_PRI,
  REPLACE_DISK_SEC,
  REPLACE_DISK_CHG,
  REPLACE_DISK_AUTO,
  ])

# Instance export mode
EXPORT_MODE_LOCAL = _constants.EXPORT_MODE_LOCAL
EXPORT_MODE_REMOTE = _constants.EXPORT_MODE_REMOTE
EXPORT_MODES = _constants.EXPORT_MODES

# instance creation modes
INSTANCE_CREATE = _constants.INSTANCE_CREATE
INSTANCE_IMPORT = _constants.INSTANCE_IMPORT
INSTANCE_REMOTE_IMPORT = _constants.INSTANCE_REMOTE_IMPORT
INSTANCE_CREATE_MODES = _constants.INSTANCE_CREATE_MODES

# Remote import/export handshake message and version
RIE_VERSION = 0
RIE_HANDSHAKE = "Hi, I'm Ganeti"

# Remote import/export certificate validity in seconds
RIE_CERT_VALIDITY = 24 * 60 * 60

# Overall timeout for establishing connection
RIE_CONNECT_TIMEOUT = 180

# Export only: how long to wait per connection attempt (seconds)
RIE_CONNECT_ATTEMPT_TIMEOUT = 20

# Export only: number of attempts to connect
RIE_CONNECT_RETRIES = 10

#: Give child process up to 5 seconds to exit after sending a signal
CHILD_LINGER_TIMEOUT = 5.0

FILE_DRIVER = compat.UniqueFrozenset([FD_LOOP, FD_BLKTAP])

# import/export config options
INISECT_EXP = "export"
INISECT_INS = "instance"
INISECT_HYP = "hypervisor"
INISECT_BEP = "backend"
INISECT_OSP = "os"

# dynamic device modification
DDM_ADD = _constants.DDM_ADD
DDM_MODIFY = _constants.DDM_MODIFY
DDM_REMOVE = _constants.DDM_REMOVE
DDMS_VALUES = _constants.DDMS_VALUES
DDMS_VALUES_WITH_MODIFY = _constants.DDMS_VALUES_WITH_MODIFY
# TODO: DDM_SWAP, DDM_MOVE?

# common exit codes
EXIT_SUCCESS = _constants.EXIT_SUCCESS
EXIT_FAILURE = _constants.EXIT_FAILURE
EXIT_NOTCLUSTER = _constants.EXIT_NOTCLUSTER
EXIT_NOTMASTER = _constants.EXIT_NOTMASTER
EXIT_NODESETUP_ERROR = _constants.EXIT_NODESETUP_ERROR
EXIT_CONFIRMATION = _constants.EXIT_CONFIRMATION # need user confirmation

#: Exit code for query operations with unknown fields
EXIT_UNKNOWN_FIELD = _constants.EXIT_UNKNOWN_FIELD

# tags
TAG_CLUSTER = _constants.TAG_CLUSTER
TAG_NODEGROUP = _constants.TAG_NODEGROUP
TAG_NODE = _constants.TAG_NODE
TAG_INSTANCE = _constants.TAG_INSTANCE
TAG_NETWORK = _constants.TAG_NETWORK
VALID_TAG_TYPES = _constants.VALID_TAG_TYPES

MAX_TAG_LEN = _constants.MAX_TAG_LEN
MAX_TAGS_PER_OBJ = _constants.MAX_TAGS_PER_OBJ

# others
DEFAULT_BRIDGE = "xen-br0"
DEFAULT_OVS = "switch1"
CLASSIC_DRBD_SYNC_SPEED = 60 * 1024  # 60 MiB, expressed in KiB
IP4_ADDRESS_LOCALHOST = "127.0.0.1"
IP4_ADDRESS_ANY = "0.0.0.0"
IP6_ADDRESS_LOCALHOST = "::1"
IP6_ADDRESS_ANY = "::"
IP4_VERSION = 4
IP6_VERSION = 6
VALID_IP_VERSIONS = compat.UniqueFrozenset([IP4_VERSION, IP6_VERSION])
# for export to htools
IP4_FAMILY = socket.AF_INET
IP6_FAMILY = socket.AF_INET6

TCP_PING_TIMEOUT = 10
DEFAULT_VG = "xenvg"
DEFAULT_DRBD_HELPER = "/bin/true"
MIN_VG_SIZE = 20480
DEFAULT_MAC_PREFIX = "aa:00:00"
# default maximum instance wait time, in seconds.
DEFAULT_SHUTDOWN_TIMEOUT = 120
NODE_MAX_CLOCK_SKEW = 150
# Time for an intra-cluster disk transfer to wait for a connection
DISK_TRANSFER_CONNECT_TIMEOUT = 60
# Disk index separator
DISK_SEPARATOR = _autoconf.DISK_SEPARATOR
IP_COMMAND_PATH = _autoconf.IP_PATH

#: Key for job IDs in opcode result
JOB_IDS_KEY = "jobs"

# runparts results
(RUNPARTS_SKIP,
 RUNPARTS_RUN,
 RUNPARTS_ERR) = range(3)

RUNPARTS_STATUS = compat.UniqueFrozenset([
  RUNPARTS_SKIP,
  RUNPARTS_RUN,
  RUNPARTS_ERR,
  ])

# RPC constants
(RPC_ENCODING_NONE,
 RPC_ENCODING_ZLIB_BASE64) = range(2)

# Various time constants for the timeout table
RPC_TMO_URGENT = 60 # one minute
RPC_TMO_FAST = 5 * 60 # five minutes
RPC_TMO_NORMAL = 15 * 60 # 15 minutes
RPC_TMO_SLOW = 3600 # one hour
RPC_TMO_4HRS = 4 * 3600
RPC_TMO_1DAY = 86400

# Timeout for connecting to nodes (seconds)
RPC_CONNECT_TIMEOUT = 5

# os related constants
OS_SCRIPT_CREATE = "create"
OS_SCRIPT_IMPORT = "import"
OS_SCRIPT_EXPORT = "export"
OS_SCRIPT_RENAME = "rename"
OS_SCRIPT_VERIFY = "verify"
OS_SCRIPTS = compat.UniqueFrozenset([
  OS_SCRIPT_CREATE,
  OS_SCRIPT_IMPORT,
  OS_SCRIPT_EXPORT,
  OS_SCRIPT_RENAME,
  OS_SCRIPT_VERIFY,
  ])

OS_API_FILE = "ganeti_api_version"
OS_VARIANTS_FILE = "variants.list"
OS_PARAMETERS_FILE = "parameters.list"

OS_VALIDATE_PARAMETERS = "parameters"
OS_VALIDATE_CALLS = compat.UniqueFrozenset([OS_VALIDATE_PARAMETERS])

# External Storage (ES) related constants
ES_ACTION_CREATE = "create"
ES_ACTION_REMOVE = "remove"
ES_ACTION_GROW = "grow"
ES_ACTION_ATTACH = "attach"
ES_ACTION_DETACH = "detach"
ES_ACTION_SETINFO = "setinfo"
ES_ACTION_VERIFY = "verify"

ES_SCRIPT_CREATE = ES_ACTION_CREATE
ES_SCRIPT_REMOVE = ES_ACTION_REMOVE
ES_SCRIPT_GROW = ES_ACTION_GROW
ES_SCRIPT_ATTACH = ES_ACTION_ATTACH
ES_SCRIPT_DETACH = ES_ACTION_DETACH
ES_SCRIPT_SETINFO = ES_ACTION_SETINFO
ES_SCRIPT_VERIFY = ES_ACTION_VERIFY
ES_SCRIPTS = frozenset([
  ES_SCRIPT_CREATE,
  ES_SCRIPT_REMOVE,
  ES_SCRIPT_GROW,
  ES_SCRIPT_ATTACH,
  ES_SCRIPT_DETACH,
  ES_SCRIPT_SETINFO,
  ES_SCRIPT_VERIFY
  ])

ES_PARAMETERS_FILE = "parameters.list"

# reboot types
INSTANCE_REBOOT_SOFT = _constants.INSTANCE_REBOOT_SOFT
INSTANCE_REBOOT_HARD = _constants.INSTANCE_REBOOT_HARD
INSTANCE_REBOOT_FULL = _constants.INSTANCE_REBOOT_FULL
REBOOT_TYPES = _constants.REBOOT_TYPES

# instance reboot behaviors
INSTANCE_REBOOT_ALLOWED = "reboot"
INSTANCE_REBOOT_EXIT = "exit"

REBOOT_BEHAVIORS = compat.UniqueFrozenset([
  INSTANCE_REBOOT_ALLOWED,
  INSTANCE_REBOOT_EXIT,
  ])

VTYPE_STRING = _constants.VTYPE_STRING
VTYPE_MAYBE_STRING = _constants.VTYPE_MAYBE_STRING
VTYPE_BOOL = _constants.VTYPE_BOOL
VTYPE_SIZE = _constants.VTYPE_SIZE
VTYPE_INT = _constants.VTYPE_INT
ENFORCEABLE_TYPES = _constants.ENFORCEABLE_TYPES

# Constant representing that the user does not specify any IP version
IFACE_NO_IP_VERSION_SPECIFIED = 0

VALID_SERIAL_SPEEDS = compat.UniqueFrozenset([
  75,
  110,
  300,
  600,
  1200,
  1800,
  2400,
  4800,
  9600,
  14400,
  19200,
  28800,
  38400,
  57600,
  115200,
  230400,
  345600,
  460800,
  ])

# HV parameter names (global namespace)
HV_BOOT_ORDER = "boot_order"
HV_CDROM_IMAGE_PATH = "cdrom_image_path"
HV_KVM_CDROM2_IMAGE_PATH = "cdrom2_image_path"
HV_KVM_FLOPPY_IMAGE_PATH = "floppy_image_path"
HV_NIC_TYPE = "nic_type"
HV_DISK_TYPE = "disk_type"
HV_KVM_CDROM_DISK_TYPE = "cdrom_disk_type"
HV_VNC_BIND_ADDRESS = "vnc_bind_address"
HV_VNC_PASSWORD_FILE = "vnc_password_file"
HV_VNC_TLS = "vnc_tls"
HV_VNC_X509 = "vnc_x509_path"
HV_VNC_X509_VERIFY = "vnc_x509_verify"
HV_KVM_SPICE_BIND = "spice_bind"
HV_KVM_SPICE_IP_VERSION = "spice_ip_version"
HV_KVM_SPICE_PASSWORD_FILE = "spice_password_file"
HV_KVM_SPICE_LOSSLESS_IMG_COMPR = "spice_image_compression"
HV_KVM_SPICE_JPEG_IMG_COMPR = "spice_jpeg_wan_compression"
HV_KVM_SPICE_ZLIB_GLZ_IMG_COMPR = "spice_zlib_glz_wan_compression"
HV_KVM_SPICE_STREAMING_VIDEO_DETECTION = "spice_streaming_video"
HV_KVM_SPICE_AUDIO_COMPR = "spice_playback_compression"
HV_KVM_SPICE_USE_TLS = "spice_use_tls"
HV_KVM_SPICE_TLS_CIPHERS = "spice_tls_ciphers"
HV_KVM_SPICE_USE_VDAGENT = "spice_use_vdagent"
HV_ACPI = "acpi"
HV_PAE = "pae"
HV_USE_BOOTLOADER = "use_bootloader"
HV_BOOTLOADER_ARGS = "bootloader_args"
HV_BOOTLOADER_PATH = "bootloader_path"
HV_KERNEL_ARGS = "kernel_args"
HV_KERNEL_PATH = "kernel_path"
HV_INITRD_PATH = "initrd_path"
HV_ROOT_PATH = "root_path"
HV_SERIAL_CONSOLE = "serial_console"
HV_SERIAL_SPEED = "serial_speed"
HV_USB_MOUSE = "usb_mouse"
HV_KEYMAP = "keymap"
HV_DEVICE_MODEL = "device_model"
HV_INIT_SCRIPT = "init_script"
HV_MIGRATION_PORT = "migration_port"
HV_MIGRATION_BANDWIDTH = "migration_bandwidth"
HV_MIGRATION_DOWNTIME = "migration_downtime"
HV_MIGRATION_MODE = "migration_mode"
HV_USE_LOCALTIME = "use_localtime"
HV_DISK_CACHE = "disk_cache"
HV_SECURITY_MODEL = "security_model"
HV_SECURITY_DOMAIN = "security_domain"
HV_KVM_FLAG = "kvm_flag"
HV_VHOST_NET = "vhost_net"
HV_KVM_USE_CHROOT = "use_chroot"
HV_CPU_MASK = "cpu_mask"
HV_MEM_PATH = "mem_path"
HV_PASSTHROUGH = "pci_pass"
HV_BLOCKDEV_PREFIX = "blockdev_prefix"
HV_REBOOT_BEHAVIOR = "reboot_behavior"
HV_CPU_TYPE = "cpu_type"
HV_CPU_CAP = "cpu_cap"
HV_CPU_WEIGHT = "cpu_weight"
HV_CPU_CORES = "cpu_cores"
HV_CPU_THREADS = "cpu_threads"
HV_CPU_SOCKETS = "cpu_sockets"
HV_SOUNDHW = "soundhw"
HV_USB_DEVICES = "usb_devices"
HV_VGA = "vga"
HV_KVM_EXTRA = "kvm_extra"
HV_KVM_MACHINE_VERSION = "machine_version"
HV_KVM_PATH = "kvm_path"
HV_VIF_TYPE = "vif_type"
HV_VIF_SCRIPT = "vif_script"
HV_XEN_CMD = "xen_cmd"
HV_VNET_HDR = "vnet_hdr"
HV_VIRIDIAN = "viridian"


HVS_PARAMETER_TYPES = {
  HV_KVM_PATH: VTYPE_STRING,
  HV_BOOT_ORDER: VTYPE_STRING,
  HV_KVM_FLOPPY_IMAGE_PATH: VTYPE_STRING,
  HV_CDROM_IMAGE_PATH: VTYPE_STRING,
  HV_KVM_CDROM2_IMAGE_PATH: VTYPE_STRING,
  HV_NIC_TYPE: VTYPE_STRING,
  HV_DISK_TYPE: VTYPE_STRING,
  HV_KVM_CDROM_DISK_TYPE: VTYPE_STRING,
  HV_VNC_PASSWORD_FILE: VTYPE_STRING,
  HV_VNC_BIND_ADDRESS: VTYPE_STRING,
  HV_VNC_TLS: VTYPE_BOOL,
  HV_VNC_X509: VTYPE_STRING,
  HV_VNC_X509_VERIFY: VTYPE_BOOL,
  HV_KVM_SPICE_BIND: VTYPE_STRING,
  HV_KVM_SPICE_IP_VERSION: VTYPE_INT,
  HV_KVM_SPICE_PASSWORD_FILE: VTYPE_STRING,
  HV_KVM_SPICE_LOSSLESS_IMG_COMPR: VTYPE_STRING,
  HV_KVM_SPICE_JPEG_IMG_COMPR: VTYPE_STRING,
  HV_KVM_SPICE_ZLIB_GLZ_IMG_COMPR: VTYPE_STRING,
  HV_KVM_SPICE_STREAMING_VIDEO_DETECTION: VTYPE_STRING,
  HV_KVM_SPICE_AUDIO_COMPR: VTYPE_BOOL,
  HV_KVM_SPICE_USE_TLS: VTYPE_BOOL,
  HV_KVM_SPICE_TLS_CIPHERS: VTYPE_STRING,
  HV_KVM_SPICE_USE_VDAGENT: VTYPE_BOOL,
  HV_ACPI: VTYPE_BOOL,
  HV_PAE: VTYPE_BOOL,
  HV_USE_BOOTLOADER: VTYPE_BOOL,
  HV_BOOTLOADER_PATH: VTYPE_STRING,
  HV_BOOTLOADER_ARGS: VTYPE_STRING,
  HV_KERNEL_PATH: VTYPE_STRING,
  HV_KERNEL_ARGS: VTYPE_STRING,
  HV_INITRD_PATH: VTYPE_STRING,
  HV_ROOT_PATH: VTYPE_MAYBE_STRING,
  HV_SERIAL_CONSOLE: VTYPE_BOOL,
  HV_SERIAL_SPEED: VTYPE_INT,
  HV_USB_MOUSE: VTYPE_STRING,
  HV_KEYMAP: VTYPE_STRING,
  HV_DEVICE_MODEL: VTYPE_STRING,
  HV_INIT_SCRIPT: VTYPE_STRING,
  HV_MIGRATION_PORT: VTYPE_INT,
  HV_MIGRATION_BANDWIDTH: VTYPE_INT,
  HV_MIGRATION_DOWNTIME: VTYPE_INT,
  HV_MIGRATION_MODE: VTYPE_STRING,
  HV_USE_LOCALTIME: VTYPE_BOOL,
  HV_DISK_CACHE: VTYPE_STRING,
  HV_SECURITY_MODEL: VTYPE_STRING,
  HV_SECURITY_DOMAIN: VTYPE_STRING,
  HV_KVM_FLAG: VTYPE_STRING,
  HV_VHOST_NET: VTYPE_BOOL,
  HV_KVM_USE_CHROOT: VTYPE_BOOL,
  HV_CPU_MASK: VTYPE_STRING,
  HV_MEM_PATH: VTYPE_STRING,
  HV_PASSTHROUGH: VTYPE_STRING,
  HV_BLOCKDEV_PREFIX: VTYPE_STRING,
  HV_REBOOT_BEHAVIOR: VTYPE_STRING,
  HV_CPU_TYPE: VTYPE_STRING,
  HV_CPU_CAP: VTYPE_INT,
  HV_CPU_WEIGHT: VTYPE_INT,
  HV_CPU_CORES: VTYPE_INT,
  HV_CPU_THREADS: VTYPE_INT,
  HV_CPU_SOCKETS: VTYPE_INT,
  HV_SOUNDHW: VTYPE_STRING,
  HV_USB_DEVICES: VTYPE_STRING,
  HV_VGA: VTYPE_STRING,
  HV_KVM_EXTRA: VTYPE_STRING,
  HV_KVM_MACHINE_VERSION: VTYPE_STRING,
  HV_VIF_TYPE: VTYPE_STRING,
  HV_VIF_SCRIPT: VTYPE_STRING,
  HV_XEN_CMD: VTYPE_STRING,
  HV_VNET_HDR: VTYPE_BOOL,
  HV_VIRIDIAN: VTYPE_BOOL,
  }

HVS_PARAMETERS = frozenset(HVS_PARAMETER_TYPES.keys())

HVS_PARAMETER_TITLES = {
  HV_ACPI: "ACPI",
  HV_BOOT_ORDER: "Boot_order",
  HV_CDROM_IMAGE_PATH: "CDROM_image_path",
  HV_DISK_TYPE: "Disk_type",
  HV_INITRD_PATH: "Initrd_path",
  HV_KERNEL_PATH: "Kernel_path",
  HV_NIC_TYPE: "NIC_type",
  HV_PAE: "PAE",
  HV_VNC_BIND_ADDRESS: "VNC_bind_address",
  HV_PASSTHROUGH: "pci_pass",
  HV_CPU_TYPE: "cpu_type",
  }

# Migration statuses
HV_MIGRATION_COMPLETED = "completed"
HV_MIGRATION_ACTIVE = "active"
HV_MIGRATION_FAILED = "failed"
HV_MIGRATION_CANCELLED = "cancelled"

HV_MIGRATION_VALID_STATUSES = compat.UniqueFrozenset([
  HV_MIGRATION_COMPLETED,
  HV_MIGRATION_ACTIVE,
  HV_MIGRATION_FAILED,
  HV_MIGRATION_CANCELLED,
  ])

HV_MIGRATION_FAILED_STATUSES = compat.UniqueFrozenset([
  HV_MIGRATION_FAILED,
  HV_MIGRATION_CANCELLED,
  ])

# KVM-specific statuses
HV_KVM_MIGRATION_VALID_STATUSES = HV_MIGRATION_VALID_STATUSES

# Node info keys
HV_NODEINFO_KEY_VERSION = "hv_version"

# Hypervisor state
HVST_MEMORY_TOTAL = "mem_total"
HVST_MEMORY_NODE = "mem_node"
HVST_MEMORY_HV = "mem_hv"
HVST_CPU_TOTAL = "cpu_total"
HVST_CPU_NODE = "cpu_node"

HVST_DEFAULTS = {
  HVST_MEMORY_TOTAL: 0,
  HVST_MEMORY_NODE: 0,
  HVST_MEMORY_HV: 0,
  HVST_CPU_TOTAL: 1,
  HVST_CPU_NODE: 1,
  }

HVSTS_PARAMETER_TYPES = {
  HVST_MEMORY_TOTAL: VTYPE_INT,
  HVST_MEMORY_NODE: VTYPE_INT,
  HVST_MEMORY_HV: VTYPE_INT,
  HVST_CPU_TOTAL: VTYPE_INT,
  HVST_CPU_NODE: VTYPE_INT,
  }

HVSTS_PARAMETERS = frozenset(HVSTS_PARAMETER_TYPES.keys())

# Disk state
DS_DISK_TOTAL = "disk_total"
DS_DISK_RESERVED = "disk_reserved"
DS_DISK_OVERHEAD = "disk_overhead"

DS_DEFAULTS = {
  DS_DISK_TOTAL: 0,
  DS_DISK_RESERVED: 0,
  DS_DISK_OVERHEAD: 0,
  }

DSS_PARAMETER_TYPES = {
  DS_DISK_TOTAL: VTYPE_INT,
  DS_DISK_RESERVED: VTYPE_INT,
  DS_DISK_OVERHEAD: VTYPE_INT,
  }

DSS_PARAMETERS = frozenset(DSS_PARAMETER_TYPES.keys())
DS_VALID_TYPES = compat.UniqueFrozenset([DT_PLAIN])

# Backend parameter names
BE_MEMORY = "memory" # deprecated and replaced by max and min mem
BE_MAXMEM = "maxmem"
BE_MINMEM = "minmem"
BE_VCPUS = "vcpus"
BE_AUTO_BALANCE = "auto_balance"
BE_ALWAYS_FAILOVER = "always_failover"
BE_SPINDLE_USE = "spindle_use"

BES_PARAMETER_TYPES = {
  BE_MAXMEM: VTYPE_SIZE,
  BE_MINMEM: VTYPE_SIZE,
  BE_VCPUS: VTYPE_INT,
  BE_AUTO_BALANCE: VTYPE_BOOL,
  BE_ALWAYS_FAILOVER: VTYPE_BOOL,
  BE_SPINDLE_USE: VTYPE_INT,
  }

BES_PARAMETER_TITLES = {
  BE_AUTO_BALANCE: "Auto_balance",
  BE_MAXMEM: "ConfigMaxMem",
  BE_MINMEM: "ConfigMinMem",
  BE_VCPUS: "ConfigVCPUs",
  }

BES_PARAMETER_COMPAT = {
  BE_MEMORY: VTYPE_SIZE,
  }
BES_PARAMETER_COMPAT.update(BES_PARAMETER_TYPES)

BES_PARAMETERS = frozenset(BES_PARAMETER_TYPES.keys())

# instance specs
ISPEC_MEM_SIZE = "memory-size"
ISPEC_CPU_COUNT = "cpu-count"
ISPEC_DISK_COUNT = "disk-count"
ISPEC_DISK_SIZE = "disk-size"
ISPEC_NIC_COUNT = "nic-count"
ISPEC_SPINDLE_USE = "spindle-use"

ISPECS_PARAMETER_TYPES = {
  ISPEC_MEM_SIZE: VTYPE_INT,
  ISPEC_CPU_COUNT: VTYPE_INT,
  ISPEC_DISK_COUNT: VTYPE_INT,
  ISPEC_DISK_SIZE: VTYPE_INT,
  ISPEC_NIC_COUNT: VTYPE_INT,
  ISPEC_SPINDLE_USE: VTYPE_INT,
  }

ISPECS_PARAMETERS = frozenset(ISPECS_PARAMETER_TYPES.keys())

ISPECS_MINMAX = "minmax"
ISPECS_MIN = "min"
ISPECS_MAX = "max"
ISPECS_STD = "std"
IPOLICY_DTS = "disk-templates"
IPOLICY_VCPU_RATIO = "vcpu-ratio"
IPOLICY_SPINDLE_RATIO = "spindle-ratio"

ISPECS_MINMAX_KEYS = compat.UniqueFrozenset([
  ISPECS_MIN,
  ISPECS_MAX,
  ])

IPOLICY_PARAMETERS = compat.UniqueFrozenset([
  IPOLICY_VCPU_RATIO,
  IPOLICY_SPINDLE_RATIO,
  ])

IPOLICY_ALL_KEYS = (IPOLICY_PARAMETERS |
                    frozenset([ISPECS_MINMAX, ISPECS_STD, IPOLICY_DTS]))

# Node parameter names
ND_OOB_PROGRAM = "oob_program"
ND_SPINDLE_COUNT = "spindle_count"
ND_EXCLUSIVE_STORAGE = "exclusive_storage"
ND_OVS = "ovs"
ND_OVS_NAME = "ovs_name"
ND_OVS_LINK = "ovs_link"

NDS_PARAMETER_TYPES = {
  ND_OOB_PROGRAM: VTYPE_STRING,
  ND_SPINDLE_COUNT: VTYPE_INT,
  ND_EXCLUSIVE_STORAGE: VTYPE_BOOL,
  ND_OVS: VTYPE_BOOL,
  ND_OVS_NAME: VTYPE_MAYBE_STRING,
  ND_OVS_LINK: VTYPE_MAYBE_STRING,
  }

NDS_PARAMETERS = frozenset(NDS_PARAMETER_TYPES.keys())

NDS_PARAMETER_TITLES = {
  ND_OOB_PROGRAM: "OutOfBandProgram",
  ND_SPINDLE_COUNT: "SpindleCount",
  ND_EXCLUSIVE_STORAGE: "ExclusiveStorage",
  ND_OVS: "OpenvSwitch",
  ND_OVS_NAME: "OpenvSwitchName",
  ND_OVS_LINK: "OpenvSwitchLink",
  }

# Logical Disks parameters
LDP_RESYNC_RATE = "resync-rate"
LDP_STRIPES = "stripes"
LDP_BARRIERS = "disabled-barriers"
LDP_NO_META_FLUSH = "disable-meta-flush"
LDP_DEFAULT_METAVG = "default-metavg"
LDP_DISK_CUSTOM = "disk-custom"
LDP_NET_CUSTOM = "net-custom"
LDP_PROTOCOL = "protocol"
LDP_DYNAMIC_RESYNC = "dynamic-resync"
LDP_PLAN_AHEAD = "c-plan-ahead"
LDP_FILL_TARGET = "c-fill-target"
LDP_DELAY_TARGET = "c-delay-target"
LDP_MAX_RATE = "c-max-rate"
LDP_MIN_RATE = "c-min-rate"
LDP_POOL = "pool"
DISK_LD_TYPES = {
  LDP_RESYNC_RATE: VTYPE_INT,
  LDP_STRIPES: VTYPE_INT,
  LDP_BARRIERS: VTYPE_STRING,
  LDP_NO_META_FLUSH: VTYPE_BOOL,
  LDP_DEFAULT_METAVG: VTYPE_STRING,
  LDP_DISK_CUSTOM: VTYPE_STRING,
  LDP_NET_CUSTOM: VTYPE_STRING,
  LDP_PROTOCOL: VTYPE_STRING,
  LDP_DYNAMIC_RESYNC: VTYPE_BOOL,
  LDP_PLAN_AHEAD: VTYPE_INT,
  LDP_FILL_TARGET: VTYPE_INT,
  LDP_DELAY_TARGET: VTYPE_INT,
  LDP_MAX_RATE: VTYPE_INT,
  LDP_MIN_RATE: VTYPE_INT,
  LDP_POOL: VTYPE_STRING,
  }
DISK_LD_PARAMETERS = frozenset(DISK_LD_TYPES.keys())

# Disk template parameters (can be set/changed by the user via gnt-cluster and
# gnt-group)
DRBD_RESYNC_RATE = "resync-rate"
DRBD_DATA_STRIPES = "data-stripes"
DRBD_META_STRIPES = "meta-stripes"
DRBD_DISK_BARRIERS = "disk-barriers"
DRBD_META_BARRIERS = "meta-barriers"
DRBD_DEFAULT_METAVG = "metavg"
DRBD_DISK_CUSTOM = "disk-custom"
DRBD_NET_CUSTOM = "net-custom"
DRBD_PROTOCOL = "protocol"
DRBD_DYNAMIC_RESYNC = "dynamic-resync"
DRBD_PLAN_AHEAD = "c-plan-ahead"
DRBD_FILL_TARGET = "c-fill-target"
DRBD_DELAY_TARGET = "c-delay-target"
DRBD_MAX_RATE = "c-max-rate"
DRBD_MIN_RATE = "c-min-rate"
LV_STRIPES = "stripes"
RBD_POOL = "pool"
DISK_DT_TYPES = {
  DRBD_RESYNC_RATE: VTYPE_INT,
  DRBD_DATA_STRIPES: VTYPE_INT,
  DRBD_META_STRIPES: VTYPE_INT,
  DRBD_DISK_BARRIERS: VTYPE_STRING,
  DRBD_META_BARRIERS: VTYPE_BOOL,
  DRBD_DEFAULT_METAVG: VTYPE_STRING,
  DRBD_DISK_CUSTOM: VTYPE_STRING,
  DRBD_NET_CUSTOM: VTYPE_STRING,
  DRBD_PROTOCOL: VTYPE_STRING,
  DRBD_DYNAMIC_RESYNC: VTYPE_BOOL,
  DRBD_PLAN_AHEAD: VTYPE_INT,
  DRBD_FILL_TARGET: VTYPE_INT,
  DRBD_DELAY_TARGET: VTYPE_INT,
  DRBD_MAX_RATE: VTYPE_INT,
  DRBD_MIN_RATE: VTYPE_INT,
  LV_STRIPES: VTYPE_INT,
  RBD_POOL: VTYPE_STRING,
  }

DISK_DT_PARAMETERS = frozenset(DISK_DT_TYPES.keys())

# OOB supported commands
OOB_POWER_ON = _constants.OOB_POWER_ON
OOB_POWER_OFF = _constants.OOB_POWER_OFF
OOB_POWER_CYCLE = _constants.OOB_POWER_CYCLE
OOB_POWER_STATUS = _constants.OOB_POWER_STATUS
OOB_HEALTH = _constants.OOB_HEALTH
OOB_COMMANDS = _constants.OOB_COMMANDS

OOB_POWER_STATUS_POWERED = _constants.OOB_POWER_STATUS_POWERED

OOB_TIMEOUT = _constants.OOB_TIMEOUT
OOB_POWER_DELAY = _constants.OOB_POWER_DELAY

OOB_STATUS_OK = _constants.OOB_STATUS_OK
OOB_STATUS_WARNING = _constants.OOB_STATUS_WARNING
OOB_STATUS_CRITICAL = _constants.OOB_STATUS_CRITICAL
OOB_STATUS_UNKNOWN = _constants.OOB_STATUS_UNKNOWN
OOB_STATUSES = _constants.OOB_STATUSES

# Instance Parameters Profile
PP_DEFAULT = "default"

# NIC_* constants are used inside the ganeti config
NIC_MODE = _constants.NIC_MODE
NIC_LINK = _constants.NIC_LINK
NIC_VLAN = _constants.NIC_VLAN

NIC_MODE_BRIDGED = _constants.NIC_MODE_BRIDGED
NIC_MODE_ROUTED = _constants.NIC_MODE_ROUTED
NIC_MODE_OVS = _constants.NIC_MODE_OVS
NIC_IP_POOL = _constants.NIC_IP_POOL
NIC_VALID_MODES = _constants.NIC_VALID_MODES

RESERVE_ACTION = "reserve"
RELEASE_ACTION = "release"

NICS_PARAMETER_TYPES = {
  NIC_MODE: VTYPE_STRING,
  NIC_LINK: VTYPE_STRING,
  NIC_VLAN: VTYPE_MAYBE_STRING,
  }

NICS_PARAMETERS = frozenset(NICS_PARAMETER_TYPES.keys())

# IDISK_* constants are used in opcodes, to create/change disks
IDISK_SIZE = "size"
IDISK_SPINDLES = "spindles"
IDISK_MODE = "mode"
IDISK_ADOPT = "adopt"
IDISK_VG = "vg"
IDISK_METAVG = "metavg"
IDISK_PROVIDER = "provider"
IDISK_NAME = "name"
IDISK_PARAMS_TYPES = {
  IDISK_SIZE: VTYPE_SIZE,
  IDISK_SPINDLES: VTYPE_INT,
  IDISK_MODE: VTYPE_STRING,
  IDISK_ADOPT: VTYPE_STRING,
  IDISK_VG: VTYPE_STRING,
  IDISK_METAVG: VTYPE_STRING,
  IDISK_PROVIDER: VTYPE_STRING,
  IDISK_NAME: VTYPE_MAYBE_STRING,
  }
IDISK_PARAMS = frozenset(IDISK_PARAMS_TYPES.keys())

# INIC_* constants are used in opcodes, to create/change nics
INIC_MAC = "mac"
INIC_IP = "ip"
INIC_MODE = "mode"
INIC_LINK = "link"
INIC_NETWORK = "network"
INIC_NAME = "name"
INIC_VLAN = "vlan"
INIC_BRIDGE = "bridge"
INIC_PARAMS_TYPES = {
  INIC_IP: VTYPE_MAYBE_STRING,
  INIC_LINK: VTYPE_STRING,
  INIC_MAC: VTYPE_STRING,
  INIC_MODE: VTYPE_STRING,
  INIC_NETWORK: VTYPE_MAYBE_STRING,
  INIC_NAME: VTYPE_MAYBE_STRING,
  INIC_VLAN: VTYPE_MAYBE_STRING,
  INIC_BRIDGE: VTYPE_MAYBE_STRING
  }
INIC_PARAMS = frozenset(INIC_PARAMS_TYPES.keys())

# Hypervisor constants
HT_XEN_PVM = _constants.HT_XEN_PVM
HT_FAKE = _constants.HT_FAKE
HT_XEN_HVM = _constants.HT_XEN_HVM
HT_KVM = _constants.HT_KVM
HT_CHROOT = _constants.HT_CHROOT
HT_LXC = _constants.HT_LXC
HYPER_TYPES = _constants.HYPER_TYPES
HTS_REQ_PORT = _constants.HTS_REQ_PORT

VNC_BASE_PORT = 5900
VNC_DEFAULT_BIND_ADDRESS = IP4_ADDRESS_ANY

# NIC types
HT_NIC_RTL8139 = "rtl8139"
HT_NIC_NE2K_PCI = "ne2k_pci"
HT_NIC_NE2K_ISA = "ne2k_isa"
HT_NIC_I82551 = "i82551"
HT_NIC_I85557B = "i82557b"
HT_NIC_I8259ER = "i82559er"
HT_NIC_PCNET = "pcnet"
HT_NIC_E1000 = "e1000"
HT_NIC_PARAVIRTUAL = HT_DISK_PARAVIRTUAL = "paravirtual"

HT_HVM_VALID_NIC_TYPES = compat.UniqueFrozenset([
  HT_NIC_RTL8139,
  HT_NIC_NE2K_PCI,
  HT_NIC_E1000,
  HT_NIC_NE2K_ISA,
  HT_NIC_PARAVIRTUAL,
  ])
HT_KVM_VALID_NIC_TYPES = compat.UniqueFrozenset([
  HT_NIC_RTL8139,
  HT_NIC_NE2K_PCI,
  HT_NIC_NE2K_ISA,
  HT_NIC_I82551,
  HT_NIC_I85557B,
  HT_NIC_I8259ER,
  HT_NIC_PCNET,
  HT_NIC_E1000,
  HT_NIC_PARAVIRTUAL,
  ])

# Vif types
# default vif type in xen-hvm
HT_HVM_VIF_IOEMU = "ioemu"
HT_HVM_VIF_VIF = "vif"
HT_HVM_VALID_VIF_TYPES = compat.UniqueFrozenset([
  HT_HVM_VIF_IOEMU,
  HT_HVM_VIF_VIF,
  ])

# Disk types
HT_DISK_IOEMU = "ioemu"
HT_DISK_IDE = "ide"
HT_DISK_SCSI = "scsi"
HT_DISK_SD = "sd"
HT_DISK_MTD = "mtd"
HT_DISK_PFLASH = "pflash"

HT_CACHE_DEFAULT = "default"
HT_CACHE_NONE = "none"
HT_CACHE_WTHROUGH = "writethrough"
HT_CACHE_WBACK = "writeback"
HT_VALID_CACHE_TYPES = compat.UniqueFrozenset([
  HT_CACHE_DEFAULT,
  HT_CACHE_NONE,
  HT_CACHE_WTHROUGH,
  HT_CACHE_WBACK,
  ])

HT_HVM_VALID_DISK_TYPES = compat.UniqueFrozenset([
  HT_DISK_PARAVIRTUAL,
  HT_DISK_IOEMU,
  ])
HT_KVM_VALID_DISK_TYPES = compat.UniqueFrozenset([
  HT_DISK_PARAVIRTUAL,
  HT_DISK_IDE,
  HT_DISK_SCSI,
  HT_DISK_SD,
  HT_DISK_MTD,
  HT_DISK_PFLASH,
  ])

# Mouse types:
HT_MOUSE_MOUSE = "mouse"
HT_MOUSE_TABLET = "tablet"

HT_KVM_VALID_MOUSE_TYPES = compat.UniqueFrozenset([
  HT_MOUSE_MOUSE,
  HT_MOUSE_TABLET,
  ])

# Boot order
HT_BO_FLOPPY = "floppy"
HT_BO_CDROM = "cdrom"
HT_BO_DISK = "disk"
HT_BO_NETWORK = "network"

HT_KVM_VALID_BO_TYPES = compat.UniqueFrozenset([
  HT_BO_FLOPPY,
  HT_BO_CDROM,
  HT_BO_DISK,
  HT_BO_NETWORK,
  ])

# SPICE lossless image compression options
HT_KVM_SPICE_LOSSLESS_IMG_COMPR_AUTO_GLZ = "auto_glz"
HT_KVM_SPICE_LOSSLESS_IMG_COMPR_AUTO_LZ = "auto_lz"
HT_KVM_SPICE_LOSSLESS_IMG_COMPR_QUIC = "quic"
HT_KVM_SPICE_LOSSLESS_IMG_COMPR_GLZ = "glz"
HT_KVM_SPICE_LOSSLESS_IMG_COMPR_LZ = "lz"
HT_KVM_SPICE_LOSSLESS_IMG_COMPR_OFF = "off"

HT_KVM_SPICE_VALID_LOSSLESS_IMG_COMPR_OPTIONS = compat.UniqueFrozenset([
  HT_KVM_SPICE_LOSSLESS_IMG_COMPR_AUTO_GLZ,
  HT_KVM_SPICE_LOSSLESS_IMG_COMPR_AUTO_LZ,
  HT_KVM_SPICE_LOSSLESS_IMG_COMPR_QUIC,
  HT_KVM_SPICE_LOSSLESS_IMG_COMPR_GLZ,
  HT_KVM_SPICE_LOSSLESS_IMG_COMPR_LZ,
  HT_KVM_SPICE_LOSSLESS_IMG_COMPR_OFF,
  ])

# SPICE lossy image compression options (valid for both jpeg and zlib-glz)
HT_KVM_SPICE_LOSSY_IMG_COMPR_AUTO = "auto"
HT_KVM_SPICE_LOSSY_IMG_COMPR_NEVER = "never"
HT_KVM_SPICE_LOSSY_IMG_COMPR_ALWAYS = "always"

HT_KVM_SPICE_VALID_LOSSY_IMG_COMPR_OPTIONS = compat.UniqueFrozenset([
  HT_KVM_SPICE_LOSSY_IMG_COMPR_AUTO,
  HT_KVM_SPICE_LOSSY_IMG_COMPR_NEVER,
  HT_KVM_SPICE_LOSSY_IMG_COMPR_ALWAYS,
  ])

# SPICE video stream detection
HT_KVM_SPICE_VIDEO_STREAM_DETECTION_OFF = "off"
HT_KVM_SPICE_VIDEO_STREAM_DETECTION_ALL = "all"
HT_KVM_SPICE_VIDEO_STREAM_DETECTION_FILTER = "filter"

HT_KVM_SPICE_VALID_VIDEO_STREAM_DETECTION_OPTIONS = compat.UniqueFrozenset([
  HT_KVM_SPICE_VIDEO_STREAM_DETECTION_OFF,
  HT_KVM_SPICE_VIDEO_STREAM_DETECTION_ALL,
  HT_KVM_SPICE_VIDEO_STREAM_DETECTION_FILTER,
  ])

# Security models
HT_SM_NONE = "none"
HT_SM_USER = "user"
HT_SM_POOL = "pool"

HT_KVM_VALID_SM_TYPES = compat.UniqueFrozenset([
  HT_SM_NONE,
  HT_SM_USER,
  HT_SM_POOL,
  ])

# Kvm flag values
HT_KVM_ENABLED = "enabled"
HT_KVM_DISABLED = "disabled"

HT_KVM_FLAG_VALUES = compat.UniqueFrozenset([HT_KVM_ENABLED, HT_KVM_DISABLED])

# Migration type
HT_MIGRATION_LIVE = _constants.HT_MIGRATION_LIVE
HT_MIGRATION_NONLIVE = _constants.HT_MIGRATION_NONLIVE
HT_MIGRATION_MODES = _constants.HT_MIGRATION_MODES

# Cluster Verify steps
VERIFY_NPLUSONE_MEM = _constants.VERIFY_NPLUSONE_MEM
VERIFY_OPTIONAL_CHECKS = _constants.VERIFY_OPTIONAL_CHECKS

# Cluster Verify error classes
CV_TCLUSTER = _constants.CV_TCLUSTER
CV_TGROUP = _constants.CV_TGROUP
CV_TNODE = _constants.CV_TNODE
CV_TINSTANCE = _constants.CV_TINSTANCE

# Cluster Verify error codes and documentation
CV_ECLUSTERCFG = _constants.CV_ECLUSTERCFG
CV_ECLUSTERCERT = _constants.CV_ECLUSTERCERT
CV_ECLUSTERFILECHECK = _constants.CV_ECLUSTERFILECHECK
CV_ECLUSTERDANGLINGNODES = _constants.CV_ECLUSTERDANGLINGNODES
CV_ECLUSTERDANGLINGINST = _constants.CV_ECLUSTERDANGLINGINST
CV_EGROUPDIFFERENTPVSIZE = _constants.CV_EGROUPDIFFERENTPVSIZE
CV_EINSTANCEBADNODE = _constants.CV_EINSTANCEBADNODE
CV_EINSTANCEDOWN = _constants.CV_EINSTANCEDOWN
CV_EINSTANCELAYOUT = _constants.CV_EINSTANCELAYOUT
CV_EINSTANCEMISSINGDISK = _constants.CV_EINSTANCEMISSINGDISK
CV_EINSTANCEFAULTYDISK = _constants.CV_EINSTANCEFAULTYDISK
CV_EINSTANCEWRONGNODE = _constants.CV_EINSTANCEWRONGNODE
CV_EINSTANCESPLITGROUPS = _constants.CV_EINSTANCESPLITGROUPS
CV_EINSTANCEPOLICY = _constants.CV_EINSTANCEPOLICY
CV_EINSTANCEUNSUITABLENODE = _constants.CV_EINSTANCEUNSUITABLENODE
CV_EINSTANCEMISSINGCFGPARAMETER = _constants.CV_EINSTANCEMISSINGCFGPARAMETER
CV_ENODEDRBD = _constants.CV_ENODEDRBD
CV_ENODEDRBDVERSION = _constants.CV_ENODEDRBDVERSION
CV_ENODEDRBDHELPER = _constants.CV_ENODEDRBDHELPER
CV_ENODEFILECHECK = _constants.CV_ENODEFILECHECK
CV_ENODEHOOKS = _constants.CV_ENODEHOOKS
CV_ENODEHV = _constants.CV_ENODEHV
CV_ENODELVM = _constants.CV_ENODELVM
CV_ENODEN1 = _constants.CV_ENODEN1
CV_ENODENET = _constants.CV_ENODENET
CV_ENODEOS = _constants.CV_ENODEOS
CV_ENODEORPHANINSTANCE = _constants.CV_ENODEORPHANINSTANCE
CV_ENODEORPHANLV = _constants.CV_ENODEORPHANLV
CV_ENODERPC = _constants.CV_ENODERPC
CV_ENODESSH = _constants.CV_ENODESSH
CV_ENODEVERSION = _constants.CV_ENODEVERSION
CV_ENODESETUP = _constants.CV_ENODESETUP
CV_ENODETIME = _constants.CV_ENODETIME
CV_ENODEOOBPATH = _constants.CV_ENODEOOBPATH
CV_ENODEUSERSCRIPTS = _constants.CV_ENODEUSERSCRIPTS
CV_ENODEFILESTORAGEPATHS = _constants.CV_ENODEFILESTORAGEPATHS
CV_ENODEFILESTORAGEPATHUNUSABLE = _constants.CV_ENODEFILESTORAGEPATHUNUSABLE
CV_ENODESHAREDFILESTORAGEPATHUNUSABLE = \
  _constants.CV_ENODESHAREDFILESTORAGEPATHUNUSABLE

CV_ALL_ECODES = _constants.CV_ALL_ECODES
CV_ALL_ECODES_STRINGS = _constants.CV_ALL_ECODES_STRINGS

# Node verify constants
NV_BRIDGES = "bridges"
NV_DRBDHELPER = "drbd-helper"
NV_DRBDVERSION = "drbd-version"
NV_DRBDLIST = "drbd-list"
NV_EXCLUSIVEPVS = "exclusive-pvs"
NV_FILELIST = "filelist"
NV_ACCEPTED_STORAGE_PATHS = "allowed-file-storage-paths"
NV_FILE_STORAGE_PATH = "file-storage-path"
NV_SHARED_FILE_STORAGE_PATH = "shared-file-storage-path"
NV_HVINFO = "hvinfo"
NV_HVPARAMS = "hvparms"
NV_HYPERVISOR = "hypervisor"
NV_INSTANCELIST = "instancelist"
NV_LVLIST = "lvlist"
NV_MASTERIP = "master-ip"
NV_NODELIST = "nodelist"
NV_NODENETTEST = "node-net-test"
NV_NODESETUP = "nodesetup"
NV_OOB_PATHS = "oob-paths"
NV_OSLIST = "oslist"
NV_PVLIST = "pvlist"
NV_TIME = "time"
NV_USERSCRIPTS = "user-scripts"
NV_VERSION = "version"
NV_VGLIST = "vglist"
NV_VMNODES = "vmnodes"

# Instance status
INSTST_RUNNING = _constants.INSTST_RUNNING
INSTST_ADMINDOWN = _constants.INSTST_ADMINDOWN
INSTST_ADMINOFFLINE = _constants.INSTST_ADMINOFFLINE
INSTST_NODEOFFLINE = _constants.INSTST_NODEOFFLINE
INSTST_NODEDOWN = _constants.INSTST_NODEDOWN
INSTST_WRONGNODE = _constants.INSTST_WRONGNODE
INSTST_ERRORUP = _constants.INSTST_ERRORUP
INSTST_ERRORDOWN = _constants.INSTST_ERRORDOWN
INSTST_ALL = _constants.INSTST_ALL

# Admin states
ADMINST_UP = _constants.ADMINST_UP
ADMINST_DOWN = _constants.ADMINST_DOWN
ADMINST_OFFLINE = _constants.ADMINST_OFFLINE
ADMINST_ALL = _constants.ADMINST_ALL

# Node roles
NR_REGULAR = _constants.NR_REGULAR
NR_MASTER = _constants.NR_MASTER
NR_MCANDIDATE = _constants.NR_MCANDIDATE
NR_DRAINED = _constants.NR_DRAINED
NR_OFFLINE = _constants.NR_OFFLINE
NR_ALL = _constants.NR_ALL

# SSL certificate check constants (in days)
SSL_CERT_EXPIRATION_WARN = 30
SSL_CERT_EXPIRATION_ERROR = 7

# Allocator framework constants
IALLOCATOR_VERSION = _constants.IALLOCATOR_VERSION
IALLOCATOR_DIR_IN = _constants.IALLOCATOR_DIR_IN
IALLOCATOR_DIR_OUT = _constants.IALLOCATOR_DIR_OUT
VALID_IALLOCATOR_DIRECTIONS = _constants.VALID_IALLOCATOR_DIRECTIONS

IALLOCATOR_MODE_ALLOC = _constants.IALLOCATOR_MODE_ALLOC
IALLOCATOR_MODE_RELOC = _constants.IALLOCATOR_MODE_RELOC
IALLOCATOR_MODE_CHG_GROUP = _constants.IALLOCATOR_MODE_CHG_GROUP
IALLOCATOR_MODE_NODE_EVAC = _constants.IALLOCATOR_MODE_NODE_EVAC
IALLOCATOR_MODE_MULTI_ALLOC = _constants.IALLOCATOR_MODE_MULTI_ALLOC
VALID_IALLOCATOR_MODES = _constants.VALID_IALLOCATOR_MODES

IALLOCATOR_SEARCH_PATH = _constants.IALLOCATOR_SEARCH_PATH
DEFAULT_IALLOCATOR_SHORTCUT = _constants.DEFAULT_IALLOCATOR_SHORTCUT

IALLOCATOR_NEVAC_PRI = _constants.IALLOCATOR_NEVAC_PRI
IALLOCATOR_NEVAC_SEC = _constants.IALLOCATOR_NEVAC_SEC
IALLOCATOR_NEVAC_ALL = _constants.IALLOCATOR_NEVAC_ALL
IALLOCATOR_NEVAC_MODES = _constants.IALLOCATOR_NEVAC_MODES

# Node evacuation
NODE_EVAC_PRI = _constants.NODE_EVAC_PRI
NODE_EVAC_SEC = _constants.NODE_EVAC_SEC
NODE_EVAC_ALL = _constants.NODE_EVAC_ALL
NODE_EVAC_MODES = _constants.NODE_EVAC_MODES

# Job queue
JOB_QUEUE_VERSION = 1
JOB_QUEUE_SIZE_HARD_LIMIT = 5000
JOB_QUEUE_FILES_PERMS = 0640

JOB_ID_TEMPLATE = r"\d+"
JOB_FILE_RE = re.compile(r"^job-(%s)$" % JOB_ID_TEMPLATE)

# unchanged job return
JOB_NOTCHANGED = "nochange"

# Job status
JOB_STATUS_QUEUED = _constants.JOB_STATUS_QUEUED
JOB_STATUS_WAITING = _constants.JOB_STATUS_WAITING
JOB_STATUS_CANCELING = _constants.JOB_STATUS_CANCELING
JOB_STATUS_RUNNING = _constants.JOB_STATUS_RUNNING
JOB_STATUS_CANCELED = _constants.JOB_STATUS_CANCELED
JOB_STATUS_SUCCESS = _constants.JOB_STATUS_SUCCESS
JOB_STATUS_ERROR = _constants.JOB_STATUS_ERROR
JOBS_PENDING = _constants.JOBS_PENDING
JOBS_FINALIZED = _constants.JOBS_FINALIZED
JOB_STATUS_ALL = _constants.JOB_STATUS_ALL

# OpCode status
# not yet finalized
OP_STATUS_QUEUED = _constants.OP_STATUS_QUEUED
OP_STATUS_WAITING = _constants.OP_STATUS_WAITING
OP_STATUS_CANCELING = _constants.OP_STATUS_CANCELING
OP_STATUS_RUNNING = _constants.OP_STATUS_RUNNING
# finalized
OP_STATUS_CANCELED = _constants.OP_STATUS_CANCELED
OP_STATUS_SUCCESS = _constants.OP_STATUS_SUCCESS
OP_STATUS_ERROR = _constants.OP_STATUS_ERROR
OPS_FINALIZED = _constants.OPS_FINALIZED

# OpCode priority
OP_PRIO_LOWEST = _constants.OP_PRIO_LOWEST
OP_PRIO_HIGHEST = _constants.OP_PRIO_HIGHEST
OP_PRIO_LOW = _constants.OP_PRIO_LOW
OP_PRIO_NORMAL = _constants.OP_PRIO_NORMAL
OP_PRIO_HIGH = _constants.OP_PRIO_HIGH
OP_PRIO_SUBMIT_VALID = _constants.OP_PRIO_SUBMIT_VALID
OP_PRIO_DEFAULT = _constants.OP_PRIO_DEFAULT

# Lock recalculate mode
LOCKS_REPLACE = "replace"
LOCKS_APPEND = "append"

# Lock timeout (sum) before we should go into blocking acquire (still
# can be reset by priority change); computed as max time (10 hours)
# before we should actually go into blocking acquire given that we
# start from default priority level; in seconds
# TODO
LOCK_ATTEMPTS_TIMEOUT = 10 * 3600 / (OP_PRIO_DEFAULT - OP_PRIO_HIGHEST)
LOCK_ATTEMPTS_MAXWAIT = 15.0
LOCK_ATTEMPTS_MINWAIT = 1.0

# Execution log types
ELOG_MESSAGE = _constants.ELOG_MESSAGE
ELOG_REMOTE_IMPORT = _constants.ELOG_REMOTE_IMPORT
ELOG_JQUEUE_TEST = _constants.ELOG_JQUEUE_TEST

# /etc/hosts modification
ETC_HOSTS_ADD = "add"
ETC_HOSTS_REMOVE = "remove"

# Job queue test
JQT_MSGPREFIX = "TESTMSG="
JQT_EXPANDNAMES = "expandnames"
JQT_EXEC = "exec"
JQT_LOGMSG = "logmsg"
JQT_STARTMSG = "startmsg"
JQT_ALL = compat.UniqueFrozenset([
  JQT_EXPANDNAMES,
  JQT_EXEC,
  JQT_LOGMSG,
  JQT_STARTMSG,
  ])

# Query resources
QR_CLUSTER = "cluster"
QR_INSTANCE = "instance"
QR_NODE = "node"
QR_LOCK = "lock"
QR_GROUP = "group"
QR_OS = "os"
QR_JOB = "job"
QR_EXPORT = "export"
QR_NETWORK = "network"
QR_EXTSTORAGE = "extstorage"

#: List of resources which can be queried using L{opcodes.OpQuery}
QR_VIA_OP = compat.UniqueFrozenset([
  QR_CLUSTER,
  QR_INSTANCE,
  QR_NODE,
  QR_GROUP,
  QR_OS,
  QR_EXPORT,
  QR_NETWORK,
  QR_EXTSTORAGE,
  ])

#: List of resources which can be queried using Local UniX Interface
QR_VIA_LUXI = QR_VIA_OP.union([
  QR_LOCK,
  QR_JOB,
  ])

#: List of resources which can be queried using RAPI
QR_VIA_RAPI = QR_VIA_LUXI

# Query field types
QFT_UNKNOWN = "unknown"
QFT_TEXT = "text"
QFT_BOOL = "bool"
QFT_NUMBER = "number"
QFT_UNIT = "unit"
QFT_TIMESTAMP = "timestamp"
QFT_OTHER = "other"

#: All query field types
QFT_ALL = compat.UniqueFrozenset([
  QFT_UNKNOWN,
  QFT_TEXT,
  QFT_BOOL,
  QFT_NUMBER,
  QFT_UNIT,
  QFT_TIMESTAMP,
  QFT_OTHER,
  ])

# Query result field status (don't change or reuse values as they're used by
# clients)
#: Normal field status
RS_NORMAL = 0
#: Unknown field
RS_UNKNOWN = 1
#: No data (e.g. RPC error), can be used instead of L{RS_OFFLINE}
RS_NODATA = 2
#: Value unavailable/unsupported for item; if this field is supported
#: but we cannot get the data for the moment, RS_NODATA or
#: RS_OFFLINE should be used
RS_UNAVAIL = 3
#: Resource marked offline
RS_OFFLINE = 4

RS_ALL = compat.UniqueFrozenset([
  RS_NORMAL,
  RS_UNKNOWN,
  RS_NODATA,
  RS_UNAVAIL,
  RS_OFFLINE,
  ])

#: Dictionary with special field cases and their verbose/terse formatting
RSS_DESCRIPTION = {
  RS_UNKNOWN: ("(unknown)", "??"),
  RS_NODATA: ("(nodata)", "?"),
  RS_OFFLINE: ("(offline)", "*"),
  RS_UNAVAIL: ("(unavail)", "-"),
  }

# max dynamic devices
MAX_NICS = 8
MAX_DISKS = 16

# SSCONF file prefix
SSCONF_FILEPREFIX = "ssconf_"
# SSCONF keys
SS_CLUSTER_NAME = "cluster_name"
SS_CLUSTER_TAGS = "cluster_tags"
SS_FILE_STORAGE_DIR = "file_storage_dir"
SS_SHARED_FILE_STORAGE_DIR = "shared_file_storage_dir"
SS_MASTER_CANDIDATES = "master_candidates"
SS_MASTER_CANDIDATES_IPS = "master_candidates_ips"
SS_MASTER_IP = "master_ip"
SS_MASTER_NETDEV = "master_netdev"
SS_MASTER_NETMASK = "master_netmask"
SS_MASTER_NODE = "master_node"
SS_NODE_LIST = "node_list"
SS_NODE_PRIMARY_IPS = "node_primary_ips"
SS_NODE_SECONDARY_IPS = "node_secondary_ips"
SS_OFFLINE_NODES = "offline_nodes"
SS_ONLINE_NODES = "online_nodes"
SS_PRIMARY_IP_FAMILY = "primary_ip_family"
SS_INSTANCE_LIST = "instance_list"
SS_RELEASE_VERSION = "release_version"
SS_HYPERVISOR_LIST = "hypervisor_list"
SS_MAINTAIN_NODE_HEALTH = "maintain_node_health"
SS_UID_POOL = "uid_pool"
SS_NODEGROUPS = "nodegroups"
SS_NETWORKS = "networks"

# This is not a complete SSCONF key, but the prefix for the hypervisor keys
SS_HVPARAMS_PREF = "hvparams_"

# Hvparams keys:
SS_HVPARAMS_XEN_PVM = SS_HVPARAMS_PREF + HT_XEN_PVM
SS_HVPARAMS_XEN_FAKE = SS_HVPARAMS_PREF + HT_FAKE
SS_HVPARAMS_XEN_HVM = SS_HVPARAMS_PREF + HT_XEN_HVM
SS_HVPARAMS_XEN_KVM = SS_HVPARAMS_PREF + HT_KVM
SS_HVPARAMS_XEN_CHROOT = SS_HVPARAMS_PREF + HT_CHROOT
SS_HVPARAMS_XEN_LXC = SS_HVPARAMS_PREF + HT_LXC

VALID_SS_HVPARAMS_KEYS = compat.UniqueFrozenset([
  SS_HVPARAMS_XEN_PVM,
  SS_HVPARAMS_XEN_FAKE,
  SS_HVPARAMS_XEN_HVM,
  SS_HVPARAMS_XEN_KVM,
  SS_HVPARAMS_XEN_CHROOT,
  SS_HVPARAMS_XEN_LXC,
  ])

SS_FILE_PERMS = 0444

# cluster wide default parameters
DEFAULT_ENABLED_HYPERVISOR = HT_XEN_PVM

HVC_DEFAULTS = {
  HT_XEN_PVM: {
    HV_USE_BOOTLOADER: False,
    HV_BOOTLOADER_PATH: XEN_BOOTLOADER,
    HV_BOOTLOADER_ARGS: "",
    HV_KERNEL_PATH: XEN_KERNEL,
    HV_INITRD_PATH: "",
    HV_ROOT_PATH: "/dev/xvda1",
    HV_KERNEL_ARGS: "ro",
    HV_MIGRATION_PORT: 8002,
    HV_MIGRATION_MODE: HT_MIGRATION_LIVE,
    HV_BLOCKDEV_PREFIX: "sd",
    HV_REBOOT_BEHAVIOR: INSTANCE_REBOOT_ALLOWED,
    HV_CPU_MASK: CPU_PINNING_ALL,
    HV_CPU_CAP: 0,
    HV_CPU_WEIGHT: 256,
    HV_VIF_SCRIPT: "",
    HV_XEN_CMD: XEN_CMD_XM,
    },
  HT_XEN_HVM: {
    HV_BOOT_ORDER: "cd",
    HV_CDROM_IMAGE_PATH: "",
    HV_NIC_TYPE: HT_NIC_RTL8139,
    HV_DISK_TYPE: HT_DISK_PARAVIRTUAL,
    HV_VNC_BIND_ADDRESS: IP4_ADDRESS_ANY,
    HV_VNC_PASSWORD_FILE: pathutils.VNC_PASSWORD_FILE,
    HV_ACPI: True,
    HV_PAE: True,
    HV_KERNEL_PATH: "/usr/lib/xen/boot/hvmloader",
    HV_DEVICE_MODEL: "/usr/lib/xen/bin/qemu-dm",
    HV_MIGRATION_PORT: 8002,
    HV_MIGRATION_MODE: HT_MIGRATION_NONLIVE,
    HV_USE_LOCALTIME: False,
    HV_BLOCKDEV_PREFIX: "hd",
    HV_PASSTHROUGH: "",
    HV_REBOOT_BEHAVIOR: INSTANCE_REBOOT_ALLOWED,
    HV_CPU_MASK: CPU_PINNING_ALL,
    HV_CPU_CAP: 0,
    HV_CPU_WEIGHT: 256,
    HV_VIF_TYPE: HT_HVM_VIF_IOEMU,
    HV_VIF_SCRIPT: "",
    HV_VIRIDIAN: False,
    HV_XEN_CMD: XEN_CMD_XM,
    },
  HT_KVM: {
    HV_KVM_PATH: KVM_PATH,
    HV_KERNEL_PATH: KVM_KERNEL,
    HV_INITRD_PATH: "",
    HV_KERNEL_ARGS: "ro",
    HV_ROOT_PATH: "/dev/vda1",
    HV_ACPI: True,
    HV_SERIAL_CONSOLE: True,
    HV_SERIAL_SPEED: 38400,
    HV_VNC_BIND_ADDRESS: "",
    HV_VNC_TLS: False,
    HV_VNC_X509: "",
    HV_VNC_X509_VERIFY: False,
    HV_VNC_PASSWORD_FILE: "",
    HV_KVM_SPICE_BIND: "",
    HV_KVM_SPICE_IP_VERSION: IFACE_NO_IP_VERSION_SPECIFIED,
    HV_KVM_SPICE_PASSWORD_FILE: "",
    HV_KVM_SPICE_LOSSLESS_IMG_COMPR: "",
    HV_KVM_SPICE_JPEG_IMG_COMPR: "",
    HV_KVM_SPICE_ZLIB_GLZ_IMG_COMPR: "",
    HV_KVM_SPICE_STREAMING_VIDEO_DETECTION: "",
    HV_KVM_SPICE_AUDIO_COMPR: True,
    HV_KVM_SPICE_USE_TLS: False,
    HV_KVM_SPICE_TLS_CIPHERS: OPENSSL_CIPHERS,
    HV_KVM_SPICE_USE_VDAGENT: True,
    HV_KVM_FLOPPY_IMAGE_PATH: "",
    HV_CDROM_IMAGE_PATH: "",
    HV_KVM_CDROM2_IMAGE_PATH: "",
    HV_BOOT_ORDER: HT_BO_DISK,
    HV_NIC_TYPE: HT_NIC_PARAVIRTUAL,
    HV_DISK_TYPE: HT_DISK_PARAVIRTUAL,
    HV_KVM_CDROM_DISK_TYPE: "",
    HV_USB_MOUSE: "",
    HV_KEYMAP: "",
    HV_MIGRATION_PORT: 8102,
    HV_MIGRATION_BANDWIDTH: 32, # MiB/s
    HV_MIGRATION_DOWNTIME: 30,  # ms
    HV_MIGRATION_MODE: HT_MIGRATION_LIVE,
    HV_USE_LOCALTIME: False,
    HV_DISK_CACHE: HT_CACHE_DEFAULT,
    HV_SECURITY_MODEL: HT_SM_NONE,
    HV_SECURITY_DOMAIN: "",
    HV_KVM_FLAG: "",
    HV_VHOST_NET: False,
    HV_KVM_USE_CHROOT: False,
    HV_MEM_PATH: "",
    HV_REBOOT_BEHAVIOR: INSTANCE_REBOOT_ALLOWED,
    HV_CPU_MASK: CPU_PINNING_ALL,
    HV_CPU_TYPE: "",
    HV_CPU_CORES: 0,
    HV_CPU_THREADS: 0,
    HV_CPU_SOCKETS: 0,
    HV_SOUNDHW: "",
    HV_USB_DEVICES: "",
    HV_VGA: "",
    HV_KVM_EXTRA: "",
    HV_KVM_MACHINE_VERSION: "",
    HV_VNET_HDR: True,
    },
  HT_FAKE: {
    HV_MIGRATION_MODE: HT_MIGRATION_LIVE,
  },
  HT_CHROOT: {
    HV_INIT_SCRIPT: "/ganeti-chroot",
    },
  HT_LXC: {
    HV_CPU_MASK: "",
    },
  }

HVC_GLOBALS = compat.UniqueFrozenset([
  HV_MIGRATION_PORT,
  HV_MIGRATION_BANDWIDTH,
  HV_MIGRATION_MODE,
  HV_XEN_CMD,
  ])

BEC_DEFAULTS = {
  BE_MINMEM: 128,
  BE_MAXMEM: 128,
  BE_VCPUS: 1,
  BE_AUTO_BALANCE: True,
  BE_ALWAYS_FAILOVER: False,
  BE_SPINDLE_USE: 1,
  }

NDC_DEFAULTS = {
  ND_OOB_PROGRAM: "",
  ND_SPINDLE_COUNT: 1,
  ND_EXCLUSIVE_STORAGE: False,
  ND_OVS: False,
  ND_OVS_NAME: DEFAULT_OVS,
  ND_OVS_LINK: ""
  }

NDC_GLOBALS = compat.UniqueFrozenset([
  ND_EXCLUSIVE_STORAGE,
  ])

DISK_LD_DEFAULTS = {
  DT_DRBD8: {
    LDP_RESYNC_RATE: CLASSIC_DRBD_SYNC_SPEED,
    LDP_BARRIERS: _autoconf.DRBD_BARRIERS,
    LDP_NO_META_FLUSH: _autoconf.DRBD_NO_META_FLUSH,
    LDP_DEFAULT_METAVG: DEFAULT_VG,
    LDP_DISK_CUSTOM: "",
    LDP_NET_CUSTOM: "",
    LDP_PROTOCOL: DRBD_DEFAULT_NET_PROTOCOL,
    LDP_DYNAMIC_RESYNC: False,

    # The default values for the DRBD dynamic resync speed algorithm
    # are taken from the drbsetup 8.3.11 man page, except for
    # c-plan-ahead (that we don't need to set to 0, because we have a
    # separate option to enable it) and for c-max-rate, that we cap to
    # the default value for the static resync rate.
    LDP_PLAN_AHEAD: 20, # ds
    LDP_FILL_TARGET: 0, # sectors
    LDP_DELAY_TARGET: 1, # ds
    LDP_MAX_RATE: CLASSIC_DRBD_SYNC_SPEED, # KiB/s
    LDP_MIN_RATE: 4 * 1024, # KiB/s
    },
  DT_PLAIN: {
    LDP_STRIPES: _autoconf.LVM_STRIPECOUNT
    },
  DT_FILE: {},
  DT_SHARED_FILE: {},
  DT_BLOCK: {},
  DT_RBD: {
    LDP_POOL: "rbd"
    },
  DT_EXT: {},
  }

# readability shortcuts
_LV_DEFAULTS = DISK_LD_DEFAULTS[DT_PLAIN]
_DRBD_DEFAULTS = DISK_LD_DEFAULTS[DT_DRBD8]

DISK_DT_DEFAULTS = {
  DT_PLAIN: {
    LV_STRIPES: DISK_LD_DEFAULTS[DT_PLAIN][LDP_STRIPES],
    },
  DT_DRBD8: {
    DRBD_RESYNC_RATE: _DRBD_DEFAULTS[LDP_RESYNC_RATE],
    DRBD_DATA_STRIPES: _LV_DEFAULTS[LDP_STRIPES],
    DRBD_META_STRIPES: _LV_DEFAULTS[LDP_STRIPES],
    DRBD_DISK_BARRIERS: _DRBD_DEFAULTS[LDP_BARRIERS],
    DRBD_META_BARRIERS: _DRBD_DEFAULTS[LDP_NO_META_FLUSH],
    DRBD_DEFAULT_METAVG: _DRBD_DEFAULTS[LDP_DEFAULT_METAVG],
    DRBD_DISK_CUSTOM: _DRBD_DEFAULTS[LDP_DISK_CUSTOM],
    DRBD_NET_CUSTOM: _DRBD_DEFAULTS[LDP_NET_CUSTOM],
    DRBD_PROTOCOL: _DRBD_DEFAULTS[LDP_PROTOCOL],
    DRBD_DYNAMIC_RESYNC: _DRBD_DEFAULTS[LDP_DYNAMIC_RESYNC],
    DRBD_PLAN_AHEAD: _DRBD_DEFAULTS[LDP_PLAN_AHEAD],
    DRBD_FILL_TARGET: _DRBD_DEFAULTS[LDP_FILL_TARGET],
    DRBD_DELAY_TARGET: _DRBD_DEFAULTS[LDP_DELAY_TARGET],
    DRBD_MAX_RATE: _DRBD_DEFAULTS[LDP_MAX_RATE],
    DRBD_MIN_RATE: _DRBD_DEFAULTS[LDP_MIN_RATE],
    },
  DT_DISKLESS: {},
  DT_FILE: {},
  DT_SHARED_FILE: {},
  DT_BLOCK: {},
  DT_RBD: {
    RBD_POOL: DISK_LD_DEFAULTS[DT_RBD][LDP_POOL]
    },
  DT_EXT: {},
  }

# we don't want to export the shortcuts
del _LV_DEFAULTS, _DRBD_DEFAULTS

NICC_DEFAULTS = {
  NIC_MODE: NIC_MODE_BRIDGED,
  NIC_LINK: DEFAULT_BRIDGE,
  NIC_VLAN: VALUE_HS_NOTHING,
  }

# All of the following values are quite arbitrarily - there are no
# "good" defaults, these must be customised per-site
ISPECS_MINMAX_DEFAULTS = {
  ISPECS_MIN: {
    ISPEC_MEM_SIZE: 128,
    ISPEC_CPU_COUNT: 1,
    ISPEC_DISK_COUNT: 1,
    ISPEC_DISK_SIZE: 1024,
    ISPEC_NIC_COUNT: 1,
    ISPEC_SPINDLE_USE: 1,
    },
  ISPECS_MAX: {
    ISPEC_MEM_SIZE: 32768,
    ISPEC_CPU_COUNT: 8,
    ISPEC_DISK_COUNT: MAX_DISKS,
    ISPEC_DISK_SIZE: 1024 * 1024,
    ISPEC_NIC_COUNT: MAX_NICS,
    ISPEC_SPINDLE_USE: 12,
    },
  }
IPOLICY_DEFAULTS = {
  ISPECS_MINMAX: [ISPECS_MINMAX_DEFAULTS],
  ISPECS_STD: {
    ISPEC_MEM_SIZE: 128,
    ISPEC_CPU_COUNT: 1,
    ISPEC_DISK_COUNT: 1,
    ISPEC_DISK_SIZE: 1024,
    ISPEC_NIC_COUNT: 1,
    ISPEC_SPINDLE_USE: 1,
    },
  IPOLICY_DTS: list(DISK_TEMPLATES),
  IPOLICY_VCPU_RATIO: 4.0,
  IPOLICY_SPINDLE_RATIO: 32.0,
  }

MASTER_POOL_SIZE_DEFAULT = 10

# Exclusive storage:
# Error margin used to compare physical disks
PART_MARGIN = .01
# Space reserved when creating instance disks
PART_RESERVED = .02

CONFD_PROTOCOL_VERSION = 1

CONFD_REQ_PING = 0
CONFD_REQ_NODE_ROLE_BYNAME = 1
CONFD_REQ_NODE_PIP_BY_INSTANCE_IP = 2
CONFD_REQ_CLUSTER_MASTER = 3
CONFD_REQ_NODE_PIP_LIST = 4
CONFD_REQ_MC_PIP_LIST = 5
CONFD_REQ_INSTANCES_IPS_LIST = 6
CONFD_REQ_NODE_DRBD = 7
CONFD_REQ_NODE_INSTANCES = 8

# Confd request query fields. These are used to narrow down queries.
# These must be strings rather than integers, because json-encoding
# converts them to strings anyway, as they're used as dict-keys.
CONFD_REQQ_LINK = "0"
CONFD_REQQ_IP = "1"
CONFD_REQQ_IPLIST = "2"
CONFD_REQQ_FIELDS = "3"

CONFD_REQFIELD_NAME = "0"
CONFD_REQFIELD_IP = "1"
CONFD_REQFIELD_MNODE_PIP = "2"

CONFD_REQS = compat.UniqueFrozenset([
  CONFD_REQ_PING,
  CONFD_REQ_NODE_ROLE_BYNAME,
  CONFD_REQ_NODE_PIP_BY_INSTANCE_IP,
  CONFD_REQ_CLUSTER_MASTER,
  CONFD_REQ_NODE_PIP_LIST,
  CONFD_REQ_MC_PIP_LIST,
  CONFD_REQ_INSTANCES_IPS_LIST,
  CONFD_REQ_NODE_DRBD,
  ])

CONFD_REPL_STATUS_OK = 0
CONFD_REPL_STATUS_ERROR = 1
CONFD_REPL_STATUS_NOTIMPLEMENTED = 2

CONFD_REPL_STATUSES = compat.UniqueFrozenset([
  CONFD_REPL_STATUS_OK,
  CONFD_REPL_STATUS_ERROR,
  CONFD_REPL_STATUS_NOTIMPLEMENTED,
  ])

(CONFD_NODE_ROLE_MASTER,
 CONFD_NODE_ROLE_CANDIDATE,
 CONFD_NODE_ROLE_OFFLINE,
 CONFD_NODE_ROLE_DRAINED,
 CONFD_NODE_ROLE_REGULAR,
 ) = range(5)

# A few common errors for confd
CONFD_ERROR_UNKNOWN_ENTRY = 1
CONFD_ERROR_INTERNAL = 2
CONFD_ERROR_ARGUMENT = 3

# Each request is "salted" by the current timestamp.
# This constants decides how many seconds of skew to accept.
# TODO: make this a default and allow the value to be more configurable
CONFD_MAX_CLOCK_SKEW = 2 * NODE_MAX_CLOCK_SKEW

# When we haven't reloaded the config for more than this amount of
# seconds, we force a test to see if inotify is betraying us. Using a
# prime number to ensure we get less chance of 'same wakeup' with
# other processes.
CONFD_CONFIG_RELOAD_TIMEOUT = 17

# If we receive more than one update in this amount of microseconds,
# we move to polling every RATELIMIT seconds, rather than relying on
# inotify, to be able to serve more requests.
CONFD_CONFIG_RELOAD_RATELIMIT = 250000

# Magic number prepended to all confd queries.
# This allows us to distinguish different types of confd protocols and handle
# them. For example by changing this we can move the whole payload to be
# compressed, or move away from json.
CONFD_MAGIC_FOURCC = "plj0"

# By default a confd request is sent to the minimum between this number and all
# MCs. 6 was chosen because even in the case of a disastrous 50% response rate,
# we should have enough answers to be able to compare more than one.
CONFD_DEFAULT_REQ_COVERAGE = 6

# Timeout in seconds to expire pending query request in the confd client
# library. We don't actually expect any answer more than 10 seconds after we
# sent a request.
CONFD_CLIENT_EXPIRE_TIMEOUT = 10

# Maximum UDP datagram size.
# On IPv4: 64K - 20 (ip header size) - 8 (udp header size) = 65507
# On IPv6: 64K - 40 (ip6 header size) - 8 (udp header size) = 65487
#   (assuming we can't use jumbo frames)
# We just set this to 60K, which should be enough
MAX_UDP_DATA_SIZE = 61440

# User-id pool minimum/maximum acceptable user-ids.
UIDPOOL_UID_MIN = 0
UIDPOOL_UID_MAX = 2 ** 32 - 1 # Assuming 32 bit user-ids

# Name or path of the pgrep command
PGREP = "pgrep"

# Name of the node group that gets created at cluster init or upgrade
INITIAL_NODE_GROUP_NAME = "default"

# Possible values for NodeGroup.alloc_policy
ALLOC_POLICY_PREFERRED = _constants.ALLOC_POLICY_PREFERRED
ALLOC_POLICY_LAST_RESORT = _constants.ALLOC_POLICY_LAST_RESORT
ALLOC_POLICY_UNALLOCABLE = _constants.ALLOC_POLICY_UNALLOCABLE
VALID_ALLOC_POLICIES = _constants.VALID_ALLOC_POLICIES

# Temporary external/shared storage parameters
BLOCKDEV_DRIVER_MANUAL = _constants.BLOCKDEV_DRIVER_MANUAL

# qemu-img path, required for ovfconverter
QEMUIMG_PATH = _autoconf.QEMUIMG_PATH

# Whether htools was enabled at compilation time
HTOOLS = _autoconf.HTOOLS
# The hail iallocator
IALLOC_HAIL = "hail"

# Fake opcodes for functions that have hooks attached to them via
# backend.RunLocalHooks
FAKE_OP_MASTER_TURNUP = "OP_CLUSTER_IP_TURNUP"
FAKE_OP_MASTER_TURNDOWN = "OP_CLUSTER_IP_TURNDOWN"

# SSH key types
SSHK_RSA = "rsa"
SSHK_DSA = "dsa"
SSHK_ALL = compat.UniqueFrozenset([SSHK_RSA, SSHK_DSA])

# SSH authorized key types
SSHAK_RSA = "ssh-rsa"
SSHAK_DSS = "ssh-dss"
SSHAK_ALL = compat.UniqueFrozenset([SSHAK_RSA, SSHAK_DSS])

# SSH setup
SSHS_CLUSTER_NAME = "cluster_name"
SSHS_SSH_HOST_KEY = "ssh_host_key"
SSHS_SSH_ROOT_KEY = "ssh_root_key"
SSHS_NODE_DAEMON_CERTIFICATE = "node_daemon_certificate"

#: Key files for SSH daemon
SSH_DAEMON_KEYFILES = {
  SSHK_RSA: (pathutils.SSH_HOST_RSA_PRIV, pathutils.SSH_HOST_RSA_PUB),
  SSHK_DSA: (pathutils.SSH_HOST_DSA_PRIV, pathutils.SSH_HOST_DSA_PUB),
  }

# Node daemon setup
NDS_CLUSTER_NAME = "cluster_name"
NDS_NODE_DAEMON_CERTIFICATE = "node_daemon_certificate"
NDS_SSCONF = "ssconf"
NDS_START_NODE_DAEMON = "start_node_daemon"

# Path generating random UUID
RANDOM_UUID_FILE = _constants.RANDOM_UUID_FILE

# Regex string for verifying a UUID
UUID_REGEX = "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"

# Auto-repair tag prefixes
AUTO_REPAIR_TAG_PREFIX = _constants.AUTO_REPAIR_TAG_PREFIX
AUTO_REPAIR_TAG_ENABLED = _constants.AUTO_REPAIR_TAG_ENABLED
AUTO_REPAIR_TAG_SUSPENDED = _constants.AUTO_REPAIR_TAG_SUSPENDED
AUTO_REPAIR_TAG_PENDING = _constants.AUTO_REPAIR_TAG_PENDING
AUTO_REPAIR_TAG_RESULT = _constants.AUTO_REPAIR_TAG_RESULT

# Auto-repair levels
AUTO_REPAIR_FIX_STORAGE = _constants.AUTO_REPAIR_FIX_STORAGE
AUTO_REPAIR_MIGRATE = _constants.AUTO_REPAIR_MIGRATE
AUTO_REPAIR_FAILOVER = _constants.AUTO_REPAIR_FAILOVER
AUTO_REPAIR_REINSTALL = _constants.AUTO_REPAIR_REINSTALL
AUTO_REPAIR_ALL_TYPES = _constants.AUTO_REPAIR_ALL_TYPES

# Auto-repair results
AUTO_REPAIR_SUCCESS = _constants.AUTO_REPAIR_SUCCESS
AUTO_REPAIR_FAILURE = _constants.AUTO_REPAIR_FAILURE
AUTO_REPAIR_ENOPERM = _constants.AUTO_REPAIR_ENOPERM
AUTO_REPAIR_ALL_RESULTS = _constants.AUTO_REPAIR_ALL_RESULTS

# The version identifier for builtin data collectors
BUILTIN_DATA_COLLECTOR_VERSION = _constants.BUILTIN_DATA_COLLECTOR_VERSION

# The reason trail opcode parameter name
OPCODE_REASON = "reason"

# The source reasons for the execution of an OpCode
OPCODE_REASON_SRC_CLIENT = "gnt:client"
OPCODE_REASON_SRC_NODED = "gnt:daemon:noded"
OPCODE_REASON_SRC_OPCODE = "gnt:opcode"
OPCODE_REASON_SRC_RLIB2 = "gnt:library:rlib2"
OPCODE_REASON_SRC_USER = "gnt:user"

OPCODE_REASON_SOURCES = compat.UniqueFrozenset([
  OPCODE_REASON_SRC_CLIENT,
  OPCODE_REASON_SRC_NODED,
  OPCODE_REASON_SRC_OPCODE,
  OPCODE_REASON_SRC_RLIB2,
  OPCODE_REASON_SRC_USER,
  ])

DISKSTATS_FILE = "/proc/diskstats"

# CPU load collector variables
STAT_FILE = "/proc/stat"
CPUAVGLOAD_BUFFER_SIZE = 150
CPUAVGLOAD_WINDOW_SIZE = 600

# Mond's variable for periodical data collection
MOND_TIME_INTERVAL = 5

# Do not re-export imported modules
del re, _vcsversion, _autoconf, _constants, socket, pathutils, compat


ALLOCATABLE_KEY = "allocatable"
FAILED_KEY = "failed"
