#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/motorola/cancunf',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    ('vendor.mediatek.hardware.videotelephony@1.0',): lib_fixup_vendor_suffix,
}


blob_fixups: blob_fixups_user_type = {
    'system_ext/priv-app/ImsService/ImsService.apk': blob_fixup()
        .apktool_patch('ims-patches'),
    ('system_ext/etc/init/init.vtservice.rc', 'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc'): blob_fixup()
        .regex_replace('start', 'enable'),
    'system_ext/lib64/libsource.so': blob_fixup()
        .add_needed('libui_shim.so'),
    ('vendor/bin/hw/android.hardware.gnss-service.mediatek', 'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    'vendor/bin/hw/android.hardware.memtrack-service.mediatek': blob_fixup()
        .replace_needed('android.hardware.memtrack-V1-ndk_platform.so', 'android.hardware.memtrack-V1-ndk.so'),
    ('vendor/bin/hw/android.hardware.media.c2@1.2-mediatek','vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b'): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    'vendor/bin/hw/android.hardware.security.keymint-service.trustonic': blob_fixup()
        .add_needed('android.hardware.security.rkp-V1-ndk.so')
        .replace_needed('android.hardware.security.keymint-V1-ndk_platform.so', 'android.hardware.security.keymint-V1-ndk.so')
        .replace_needed('android.hardware.security.sharedsecret-V1-ndk_platform.so', 'android.hardware.security.sharedsecret-V1-ndk.so')
        .replace_needed('android.hardware.security.secureclock-V1-ndk_platform.so', 'android.hardware.security.secureclock-V1-ndk.so'),
    ('vendor/bin/mnld', 'vendor/lib64/hw/android.hardware.sensors@2.X-subhal-mediatek.so', 'vendor/lib64/mt6855/libcam.utils.sensorprovider.so'): blob_fixup()
        .add_needed('libshim_sensors.so'),
    'vendor/lib64/hw/mt6855/vendor.mediatek.hardware.pq@2.15-impl.so': blob_fixup()
        .add_needed('libshim_sensors.so')
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libutils.so','libutils-v32.so')
        .replace_needed('libalsautils.so','libalsautils-v31.so'),
    ('vendor/lib64/hw/mt6855/android.hardware.camera.provider@2.6-impl-mediatek.so','vendor/lib64/mt6855/libmtkcam_stdutils.so',
     'vendor/lib64/sensors.moto.so'): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    ('vendor/lib64/mt6855/lib3a.flash.so', 'vendor/lib64/mt6855/lib3a.ae.stat.so', 
     'vendor/lib64/mt6855/lib3a.sensors.flicker.so', 'vendor/lib64/mt6855/lib3a.sensors.color.so', 
     'vendor/lib64/mt6855/libaaa_ltm.so', 'vendor/lib64/lib3a.ae.pipe.so'): blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/mt6855/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    ('vendor/lib64/libdlbdsservice.so', 'vendor/lib64/libcodec2_soft_ddpdec.so',
     'vendor/lib64/soundfx/libswdap.so','vendor/lib64/soundfx/libdlbvol.so',
     'vendor/lib64/libcodec2_soft_ac4dec.so','vendor/bin/hw/vendor.dolby.hardware.dms@2.0-service'): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'cancunf',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()