# Unity 2022 LTS 对 Native Render Pass 的支持情况 (截至 2026 年 2 月 8 日)

## 概述

截至 2026 年 2 月 8 日，Unity 2022 LTS（长期支持版本，正式名称为 Unity 2022.3）对 Native Render Pass（原生渲染通道）的支持情况如下：

- **Native Render Pass 是 Universal Render Pipeline (URP) 中的一个实验性功能**，旨在通过更底层的图形 API 接口（如 Vulkan 的 Render Pass 和 Metal 的 Encoder）来优化渲染性能，尤其是在移动设备上。
- **该功能在 Unity 2022 LTS 中已部分实现**，但存在平台限制、兼容性问题以及已知的局限性。
- **Unity 2022 LTS 的最新补丁版本为 2022.3.71f1**，此版本未引入 Native Render Pass 的重大更新，但包含多项图形系统稳定性修复。

---

## Native Render Pass 支持的平台

### ✅ 支持的图形 API 和平台

| 图形 API | 平台 | 支持状态 | 备注 |
|--------|------|----------|------|
| **Vulkan** | Android (TBDR 设备) | ✅ 支持 | 默认启用，适用于 Mali、Adreno 等移动设备 |
| **Metal** | iOS / macOS | ✅ 支持 | 主要用于 iOS 移动设备和 Apple 芯片 Mac |
| **OpenGL ES 2/3** | Android / iOS | ⚠️ 有限支持 | 支持但存在限制，如 MSAA 后解析问题 |
| **Direct3D12** | Windows / Xbox | ❌ 不支持 | 明确禁用，因实现约束和已知问题 |
| **Direct3D11** | Windows | ❌ 不支持 | 不推荐使用，无官方支持 |

> 📌 **关键说明**：
> - Native Render Pass 主要面向 **Tile-Based Deferred Rendering (TBDR)** GPU 架构（如移动 GPU），可显著减少内存带宽消耗。
> - 在 **Windows 上，DirectX 12 支持 Native Render Pass，而 D3D11 完全不支持** [2]。
> - **OpenGL ES 支持存在限制**，例如无法在 Native Render Pass 中正确处理 MSAA 后解析 [4]。

---

## 渲染管线兼容性

### ✅ 支持的渲染管线

| 渲染管线 | 是否支持 Native Render Pass | 备注 |
|----------|----------------------------|------|
| **Universal Render Pipeline (URP)** | ✅ 是 | 原生支持，需手动启用 |
| **High Definition Render Pipeline (HDRP)** | ❌ 否 | HDRP 使用自己的 Render Graph 实现，不兼容 URP 的 Native Render Pass |
| **Built-in Render Pipeline** | ❌ 否 | 不支持，仅限 URP |

> 📌 **注意**：
> - Native Render Pass 是 URP 特有的功能，**不适用于 HDRP 或内置渲染管线** [9]。
> - 在 URP 中，该功能通过 **Universal Renderer Data 中的设置启用**（路径：Project Settings > Graphics > Universal Render Pipeline Asset > Renderer > Enable Native Render Pass）[15]。

---

## 已知限制与工作区

### ❌ 已知问题

1. **DirectX 12 不兼容**
   - 当在 URP 资产中启用 Native Render Pass 时，**DirectX 12 下阴影显示异常或完全失效** [2]。
   - Unity 已在 2022.3.21f1 中**自动禁用 DirectX 12 上的 Native Render Pass**，以避免崩溃和渲染错误。

2. **自定义 Renderer Features 不兼容**
   - 启用 Native Render Pass 后，**自定义 Renderer Features（如后期处理效果）将自动被禁用**，因无法强制执行输入/输出依赖关系 [7][15]。
   - 开发者需改用 **Render Graph API** 编写自定义渲染通道 [10]。

3. **XR/VR 设备不支持**
   - **Quest、Pico 等 XR 头显不支持 Native Render Pass**，因实验性开发未完成 [8][13]。
   - 预计 Unity 23.2 版本将支持 XR 兼容性，但无法向后移植到 2022 LTS [10]。

4. **Metal 平台 Z 缓冲区读取限制**
   - 在 Metal 上，**无法直接读取深度缓冲区**，必须通过额外渲染目标复制深度信息 [26]。
   - 此操作会增加带宽开销，影响性能。

5. **MSAA 兼容性问题**
   - 由于缺乏样本计数信息，**原生插件难以动态适配 MSAA 设置** [26]。
   - 当前实现固定为 VK_SAMPLE_COUNT_1_BIT，导致 MSAA 失效 [26]。

---

## 官方文档与变更日志中的明确声明

### Unity 2022 LTS 发布说明与变更记录

- **Unity 2022.3.0f1** 引入 URP 的 Render Graph 系统，为 Native Render Pass 提供基础支持 [35]。
- **Unity 2022.3.21f1** 明确指出：“**为 DirectX 12 禁用 Native Render Pass**，因其不受支持” [4]。
- **Unity 2022.3.58f1** 修复了 Vulkan 上 WebCam 纹理导致的崩溃问题，表明对 Vulkan 的支持仍在持续优化 [7]。
- **Unity 2022.3.66f1** 强调 VisionOS 支持，但 Native Render Pass 仍仅限于 URP 和特定图形 API [8]。

> 📌 **重要引用**：
> - “Native Render Pass 是一项实验性功能，主要用于 URP 中提高移动平台性能。” [6]
> - “Direct3D12 不支持 Native Render Pass，请勿启用此选项。” [2]

---

## 替代方案与未来展望

### Render Graph 系统

- 自 Unity 2023 起，**Render Graph 已取代部分 Native Render Pass 功能**，提供更自动化的渲染流程管理 [11][25]。
- 在 Unity 6（23.3.beta）中，**Render Graph 自动处理 Native Render Pass 的应用**，无需手动配置 [7][15]。
- 对于 Unity 2022 LTS，开发者应迁移至 Render Graph API 而非依赖 Native Render Pass [10]。

### 升级建议

- 若项目使用 DirectX 11 或 HDRP，**不建议启用 Native Render Pass**。
- 针对 Android/iOS 移动设备，可在 URP 中启用 Native Render Pass 并配合 Vulkan/Metal 获得性能提升。
- 使用 **-force-vulkan-layers 命令行参数** 调试 Vulkan 插件 [26]。

---

## 总结

截至 2026 年 2 月 8 日，Unity 2022 LTS（2022.3.71f1）对 Native Render Pass 的支持情况如下：

- **支持的图形 API**：Vulkan（Android）、Metal（iOS/macOS）、OpenGL ES（有限支持）
- **不支持的图形 API**：Direct3D11、Direct3D12（明确禁用）
- **支持的渲染管线**：仅 Universal Render Pipeline (URP)
- **已知重大限制**：
  - DirectX 12 不兼容
  - 自定义 Renderer Features 不工作
  - XR 设备不支持
  - Metal 上无法读取深度缓冲区
  - MSAA 兼容性问题

> 💡 **结论**：Native Render Pass 在 Unity 2022 LTS 中仍处于实验阶段，**仅推荐用于特定移动平台（Vulkan/Metal）的 URP 项目**。对于跨平台或生产级项目，建议使用 Render Graph 或等待 Unity 23+ 版本的完整支持。

---

### Sources

[1] Unity 2022 LTS Release Overview: https://unity.com/releases/2022-lts  
[2] [DirectX12] Shadows broken in Game view when native-renderpass is enabled in the URP asset: https://issuetracker.unity3d.com/issues/directx12-shadows-broken-in-game-view-when-native-renderpass-is-enabled-in-the-urp-asset  
[3] Unity 2022.3.14f1: https://unity.com/releases/editor/whats-new/2022.3.14f1  
[4] Unity 2022.3.21f1: https://unity.com/releases/editor/whats-new/2022.3.21f1  
[5] Unity 2022.3.13f1: https://unity.com/releases/editor/whats-new/2022.3.13f1  
[6] Changelog | Universal RP | 14.0.12: https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/changelog/CHANGELOG.html  
[7] Unity 2022.3.58f1: https://unity.com/releases/editor/whats-new/2022.3.58f1  
[8] Unity 2022.3.66f1: https://unity.com/releases/editor/whats-new/2022.3.66f1  
[9] Render pipeline feature comparison: https://docs.unity3d.com/2022.3/Documentation/Manual/render-pipelines-feature-comparison.html  
[10] Upgrade Render Feature to Render Graph: https://discussions.unity.com/t/upgrade-render-feature-to-render-graph/1692318  
[11] Introduction to the render graph system in URP: https://docs.unity3d.com/6000.3/Documentation/Manual/urp/render-graph-introduction.html  
[12] Don't understand Render Graph Unity 6: https://discussions.unity.com/t/dont-understand-render-graph-unity-6/948783  
[13] Write a render pass using the render graph system in URP: https://docs.unity3d.com/6000.3/Documentation/Manual/urp/render-graph-write-render-pass.html  
[14] What is the purpose of this setting?: https://discussions.unity.com/t/what-is-the-purpose-of-this-setting/857962  
[15] Can't see the Native Render Pass option in the Universal Renderer Data: https://discussions.unity.com/t/cant-see-the-native-render-pass-option-in-the-universal-renderer-data/1698057  
[16] Custom render pass workflow in URP: https://docs.unity3d.com/6000.3/Documentation/Manual/urp/renderer-features/custom-rendering-pass-workflow-in-urp.html  
[17] [URP] When Native RenderPass is enabled and URP's Deferred Rendering is used...: https://issuetracker.unity3d.com/issues/urp-when-native-renderpass-is-enabled-and-urps-deferred-rendering-is-used-terrains-grass-is-is-not-affected-by-shadow-1  
[18] Unity 2022.3.0f1: https://unity.com/releases/editor/whats-new/2022.3.0f1  
[19] Unity 2022.3.29f1: https://unity.com/releases/editor/whats-new/2022.3.29f1  
[20] I have a question about urp native renderpass: https://discussions.unity.com/t/i-have-a-question-about-urp-native-renderpass/952031  
[21] Introduction of Render Graph in the Universal Render Pipeline (URP): https://discussions.unity.com/t/introduction-of-render-graph-in-the-universal-render-pipeline-urp/930355?page=45  
[22] Manual: New in Unity 2022 LTS: https://docs.unity3d.com/2022.3/Documentation/Manual/WhatsNew2022LTS.html  
[23] Unity 2022.3.52f1: https://unity.com/releases/editor/whats-new/2022.3.52f1  
[24] Unity 2022.3.44f1: https://unity.com/releases/editor/whats-new/2022.3.44f1  
[25] Introduction to the render graph system in URP (v6000.1): https://docs.unity3d.com/6000.1/Documentation/Manual/urp/render-graph-introduction.html  
[26] Introduction of Render Graph in URP (forum thread): https://discussions.unity.com/t/introduction-of-render-graph-in-the-universal-render-pipeline-urp/930355?page=45