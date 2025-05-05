/*
 * Copyright (C) The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

 #include "HalProxyCancunf.h"

 #include <ConvertUtils.h>
  
 namespace aidl {
 namespace android {
 namespace hardware {
 namespace sensors {
 namespace implementation {
 
 ndk::ScopedAStatus HalProxyCancunf::getSensorsList(
         std::vector<::aidl::android::hardware::sensors::SensorInfo>* _aidl_return) {
     for (const auto& sensor : HalProxy::getSensors()) {
      SensorInfo dst = sensor.second;

      if (dst.typeAsString != "com.motorola.sensor.double_tap" || dst.typeAsString != "com.motorola.sensor.tap") {
           _aidl_return->push_back(convertSensorInfo(dst));
        }
     }
 
     return ndk::ScopedAStatus::ok();
 }
 
 }  // namespace implementation
 }  // namespace sensors
 }  // namespace hardware
 }  // namespace android
 }  // namespace aidl
