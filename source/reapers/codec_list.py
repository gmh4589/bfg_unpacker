
codec_list = {'A8_UNORM': {'bpp': b'\x08\x00\x00\x00',
                           'codec': b'\x00\x00\x00\x00',
                           'flags': b'\x02\x00\x00\x00',
                           'head_flg': b'\x0f\x10\x02\x00',
                           'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00'},
              'AYUV': {'bpp': b'\x00\x00\x00\x00',
                       'codec': b'DX10',
                       'flags': b'\x04\x00\x00\x00',
                       'head_flg': b'\x0f\x10\x02\x00',
                       'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'B4G4R4A4_UNORM': {'bpp': b'\x10\x00\x00\x00',
                                 'codec': b'\x00\x00\x00\x00',
                                 'flags': b'A\x00\x00\x00',
                                 'head_flg': b'\x0f\x10\x02\x00',
                                 'rgb_mask': b'\x00\x0f\x00\x00\xf0\x00\x00\x00\x0f\x00\x00\x00\x00\xf0\x00\x00'},
              'B5G5R5A1_UNORM': {'bpp': b'\x10\x00\x00\x00',
                                 'codec': b'\x00\x00\x00\x00',
                                 'flags': b'A\x00\x00\x00',
                                 'head_flg': b'\x0f\x10\x02\x00',
                                 'rgb_mask': b'\x00|\x00\x00\xe0\x03\x00\x00\x1f\x00\x00\x00\x00\x80\x00\x00'},
              'B5G6R5_UNORM': {'bpp': b'\x10\x00\x00\x00',
                               'codec': b'\x00\x00\x00\x00',
                               'flags': b'@\x00\x00\x00',
                               'head_flg': b'\x0f\x10\x02\x00',
                               'rgb_mask': b'\x00\xf8\x00\x00\xe0\x07\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00'},
              'B8G8R8A8_UNORM': {'bpp': b' \x00\x00\x00',
                                 'codec': b'\x00\x00\x00\x00',
                                 'flags': b'A\x00\x00\x00',
                                 'head_flg': b'\x0f\x10\x02\x00',
                                 'rgb_mask': b'\x00\x00\xff\x00\x00\xff\x00\x00\xff\x00\x00\x00\x00\x00\x00\xff'},
              'B8G8R8A8_UNORM_SRGB': {'bpp': b'\x00\x00\x00\x00',
                                      'codec': b'DX10',
                                      'flags': b'\x04\x00\x00\x00',
                                      'head_flg': b'\x0f\x10\x02\x00',
                                      'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'B8G8R8X8_UNORM': {'bpp': b' \x00\x00\x00',
                                 'codec': b'\x00\x00\x00\x00',
                                 'flags': b'@\x00\x00\x00',
                                 'head_flg': b'\x0f\x10\x02\x00',
                                 'rgb_mask': b'\x00\x00\xff\x00\x00\xff\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00'},
              'B8G8R8X8_UNORM_SRGB': {'bpp': b'\x00\x00\x00\x00',
                                      'codec': b'DX10',
                                      'flags': b'\x04\x00\x00\x00',
                                      'head_flg': b'\x0f\x10\x02\x00',
                                      'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC1_UNORM': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'DXT1',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC1_UNORM_SRGB': {'bpp': b'\x00\x00\x00\x00',
                                 'codec': b'DX10',
                                 'flags': b'\x04\x00\x00\x00',
                                 'head_flg': b'\x07\x10\n\x00',
                                 'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC2_UNORM': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'DXT3',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC2_UNORM_SRGB': {'bpp': b'\x00\x00\x00\x00',
                                 'codec': b'DX10',
                                 'flags': b'\x04\x00\x00\x00',
                                 'head_flg': b'\x07\x10\n\x00',
                                 'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC3_UNORM': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'DXT5',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC3_UNORM_SRGB': {'bpp': b'\x00\x00\x00\x00',
                                 'codec': b'DX10',
                                 'flags': b'\x04\x00\x00\x00',
                                 'head_flg': b'\x07\x10\n\x00',
                                 'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC4_SNORM': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'BC4S',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC4_UNORM': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'BC4U',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC5_SNORM': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'BC5S',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC5_UNORM': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'BC5U',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC6H_SF16': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'DX10',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC6H_UF16': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'DX10',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC7_UNORM': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'DX10',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x07\x10\n\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'BC7_UNORM_SRGB': {'bpp': b'\x00\x00\x00\x00',
                                 'codec': b'DX10',
                                 'flags': b'\x04\x00\x00\x00',
                                 'head_flg': b'\x07\x10\n\x00',
                                 'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'G8R8_G8B8_UNORM': {'bpp': b'\x00\x00\x00\x00',
                                  'codec': b'GRGB',
                                  'flags': b'\x04\x00\x00\x00',
                                  'head_flg': b'\x0f\x10\x02\x00',
                                  'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R10G10B10A2_UINT': {'bpp': b'\x00\x00\x00\x00',
                                   'codec': b'DX10',
                                   'flags': b'\x04\x00\x00\x00',
                                   'head_flg': b'\x0f\x10\x02\x00',
                                   'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R10G10B10A2_UNORM': {'bpp': b'\x00\x00\x00\x00',
                                    'codec': b'DX10',
                                    'flags': b'\x04\x00\x00\x00',
                                    'head_flg': b'\x0f\x10\x02\x00',
                                    'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R10G10B10_XR_BIAS_A2_UNORM': {'bpp': b'\x00\x00\x00\x00',
                                             'codec': b'DX10',
                                             'flags': b'\x04\x00\x00\x00',
                                             'head_flg': b'\x0f\x10\x02\x00',
                                             'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R11G11B10_FLOAT': {'bpp': b'\x00\x00\x00\x00',
                                  'codec': b'DX10',
                                  'flags': b'\x04\x00\x00\x00',
                                  'head_flg': b'\x0f\x10\x02\x00',
                                  'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16B16A16_FLOAT': {'bpp': b'\x00\x00\x00\x00',
                                     'codec': b'q\x00\x00\x00',
                                     'flags': b'\x04\x00\x00\x00',
                                     'head_flg': b'\x0f\x10\x02\x00',
                                     'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16B16A16_SINT': {'bpp': b'\x00\x00\x00\x00',
                                    'codec': b'DX10',
                                    'flags': b'\x04\x00\x00\x00',
                                    'head_flg': b'\x0f\x10\x02\x00',
                                    'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16B16A16_SNORM': {'bpp': b'\x00\x00\x00\x00',
                                     'codec': b'n\x00\x00\x00',
                                     'flags': b'\x04\x00\x00\x00',
                                     'head_flg': b'\x0f\x10\x02\x00',
                                     'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16B16A16_UINT': {'bpp': b'\x00\x00\x00\x00',
                                    'codec': b'DX10',
                                    'flags': b'\x04\x00\x00\x00',
                                    'head_flg': b'\x0f\x10\x02\x00',
                                    'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16B16A16_UNORM': {'bpp': b'\x00\x00\x00\x00',
                                     'codec': b'$\x00\x00\x00',
                                     'flags': b'\x04\x00\x00\x00',
                                     'head_flg': b'\x0f\x10\x02\x00',
                                     'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16_FLOAT': {'bpp': b'\x00\x00\x00\x00',
                               'codec': b'p\x00\x00\x00',
                               'flags': b'\x04\x00\x00\x00',
                               'head_flg': b'\x0f\x10\x02\x00',
                               'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16_SINT': {'bpp': b'\x00\x00\x00\x00',
                              'codec': b'DX10',
                              'flags': b'\x04\x00\x00\x00',
                              'head_flg': b'\x0f\x10\x02\x00',
                              'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16_SNORM': {'bpp': b' \x00\x00\x00',
                               'codec': b'\x00\x00\x00\x00',
                               'flags': b'\x00\x00\x08\x00',
                               'head_flg': b'\x0f\x10\x02\x00',
                               'rgb_mask': b'\xff\xff\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16_UINT': {'bpp': b'\x00\x00\x00\x00',
                              'codec': b'DX10',
                              'flags': b'\x04\x00\x00\x00',
                              'head_flg': b'\x0f\x10\x02\x00',
                              'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16G16_UNORM': {'bpp': b' \x00\x00\x00',
                               'codec': b'\x00\x00\x00\x00',
                               'flags': b'@\x00\x00\x00',
                               'head_flg': b'\x0f\x10\x02\x00',
                               'rgb_mask': b'\xff\xff\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16_FLOAT': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'o\x00\x00\x00',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x0f\x10\x02\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16_SINT': {'bpp': b'\x00\x00\x00\x00',
                           'codec': b'DX10',
                           'flags': b'\x04\x00\x00\x00',
                           'head_flg': b'\x0f\x10\x02\x00',
                           'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16_SNORM': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'DX10',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x0f\x10\x02\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16_UINT': {'bpp': b'\x00\x00\x00\x00',
                           'codec': b'DX10',
                           'flags': b'\x04\x00\x00\x00',
                           'head_flg': b'\x0f\x10\x02\x00',
                           'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R16_UNORM': {'bpp': b'\x10\x00\x00\x00',
                            'codec': b'\x00\x00\x00\x00',
                            'flags': b'\x00\x00\x02\x00',
                            'head_flg': b'\x0f\x10\x02\x00',
                            'rgb_mask': b'\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32G32B32A32_FLOAT': {'bpp': b'\x00\x00\x00\x00',
                                     'codec': b't\x00\x00\x00',
                                     'flags': b'\x04\x00\x00\x00',
                                     'head_flg': b'\x0f\x10\x02\x00',
                                     'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32G32B32A32_SINT': {'bpp': b'\x00\x00\x00\x00',
                                    'codec': b'DX10',
                                    'flags': b'\x04\x00\x00\x00',
                                    'head_flg': b'\x0f\x10\x02\x00',
                                    'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32G32B32A32_UINT': {'bpp': b'\x00\x00\x00\x00',
                                    'codec': b'DX10',
                                    'flags': b'\x04\x00\x00\x00',
                                    'head_flg': b'\x0f\x10\x02\x00',
                                    'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32G32B32_FLOAT': {'bpp': b'\x00\x00\x00\x00',
                                  'codec': b'DX10',
                                  'flags': b'\x04\x00\x00\x00',
                                  'head_flg': b'\x0f\x10\x02\x00',
                                  'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32G32B32_SINT': {'bpp': b'\x00\x00\x00\x00',
                                 'codec': b'DX10',
                                 'flags': b'\x04\x00\x00\x00',
                                 'head_flg': b'\x0f\x10\x02\x00',
                                 'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32G32B32_UINT': {'bpp': b'\x00\x00\x00\x00',
                                 'codec': b'DX10',
                                 'flags': b'\x04\x00\x00\x00',
                                 'head_flg': b'\x0f\x10\x02\x00',
                                 'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32G32_FLOAT': {'bpp': b'\x00\x00\x00\x00',
                               'codec': b's\x00\x00\x00',
                               'flags': b'\x04\x00\x00\x00',
                               'head_flg': b'\x0f\x10\x02\x00',
                               'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32G32_SINT': {'bpp': b'\x00\x00\x00\x00',
                              'codec': b'DX10',
                              'flags': b'\x04\x00\x00\x00',
                              'head_flg': b'\x0f\x10\x02\x00',
                              'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32G32_UINT': {'bpp': b'\x00\x00\x00\x00',
                              'codec': b'DX10',
                              'flags': b'\x04\x00\x00\x00',
                              'head_flg': b'\x0f\x10\x02\x00',
                              'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32_FLOAT': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'r\x00\x00\x00',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x0f\x10\x02\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32_SINT': {'bpp': b'\x00\x00\x00\x00',
                           'codec': b'DX10',
                           'flags': b'\x04\x00\x00\x00',
                           'head_flg': b'\x0f\x10\x02\x00',
                           'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R32_UINT': {'bpp': b'\x00\x00\x00\x00',
                           'codec': b'DX10',
                           'flags': b'\x04\x00\x00\x00',
                           'head_flg': b'\x0f\x10\x02\x00',
                           'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8G8B8A8_SINT': {'bpp': b'\x00\x00\x00\x00',
                                'codec': b'DX10',
                                'flags': b'\x04\x00\x00\x00',
                                'head_flg': b'\x0f\x10\x02\x00',
                                'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8G8B8A8_SNORM': {'bpp': b' \x00\x00\x00',
                                 'codec': b'\x00\x00\x00\x00',
                                 'flags': b'\x00\x00\x08\x00',
                                 'head_flg': b'\x0f\x10\x02\x00',
                                 'rgb_mask': b'\xff\x00\x00\x00\x00\xff\x00\x00\x00\x00\xff\x00\x00\x00\x00\xff'},
              'R8G8B8A8_UINT': {'bpp': b'\x00\x00\x00\x00',
                                'codec': b'DX10',
                                'flags': b'\x04\x00\x00\x00',
                                'head_flg': b'\x0f\x10\x02\x00',
                                'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8G8B8A8_UNORM': {'bpp': b' \x00\x00\x00',
                                 'codec': b'\x00\x00\x00\x00',
                                 'flags': b'A\x00\x00\x00',
                                 'head_flg': b'\x0f\x10\x02\x00',
                                 'rgb_mask': b'\xff\x00\x00\x00\x00\xff\x00\x00\x00\x00\xff\x00\x00\x00\x00\xff'},
              'R8G8B8A8_UNORM_SRGB': {'bpp': b'\x00\x00\x00\x00',
                                      'codec': b'DX10',
                                      'flags': b'\x04\x00\x00\x00',
                                      'head_flg': b'\x0f\x10\x02\x00',
                                      'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8G8_B8G8_UNORM': {'bpp': b'\x00\x00\x00\x00',
                                  'codec': b'RGBG',
                                  'flags': b'\x04\x00\x00\x00',
                                  'head_flg': b'\x0f\x10\x02\x00',
                                  'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8G8_SINT': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'DX10',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x0f\x10\x02\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8G8_SNORM': {'bpp': b'\x10\x00\x00\x00',
                             'codec': b'\x00\x00\x00\x00',
                             'flags': b'\x00\x00\x08\x00',
                             'head_flg': b'\x0f\x10\x02\x00',
                             'rgb_mask': b'\xff\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8G8_UINT': {'bpp': b'\x00\x00\x00\x00',
                            'codec': b'DX10',
                            'flags': b'\x04\x00\x00\x00',
                            'head_flg': b'\x0f\x10\x02\x00',
                            'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8G8_UNORM': {'bpp': b'\x10\x00\x00\x00',
                             'codec': b'\x00\x00\x00\x00',
                             'flags': b'\x01\x00\x02\x00',
                             'head_flg': b'\x0f\x10\x02\x00',
                             'rgb_mask': b'\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00'},
              'R8_SINT': {'bpp': b'\x00\x00\x00\x00',
                          'codec': b'DX10',
                          'flags': b'\x04\x00\x00\x00',
                          'head_flg': b'\x0f\x10\x02\x00',
                          'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8_SNORM': {'bpp': b'\x00\x00\x00\x00',
                           'codec': b'DX10',
                           'flags': b'\x04\x00\x00\x00',
                           'head_flg': b'\x0f\x10\x02\x00',
                           'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8_UINT': {'bpp': b'\x00\x00\x00\x00',
                          'codec': b'DX10',
                          'flags': b'\x04\x00\x00\x00',
                          'head_flg': b'\x0f\x10\x02\x00',
                          'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R8_UNORM': {'bpp': b'\x08\x00\x00\x00',
                           'codec': b'\x00\x00\x00\x00',
                           'flags': b'\x00\x00\x02\x00',
                           'head_flg': b'\x0f\x10\x02\x00',
                           'rgb_mask': b'\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'R9G9B9E5_SHAREDEXP': {'bpp': b'\x00\x00\x00\x00',
                                     'codec': b'DX10',
                                     'flags': b'\x04\x00\x00\x00',
                                     'head_flg': b'\x0f\x10\x02\x00',
                                     'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'Y210': {'bpp': b'\x00\x00\x00\x00',
                       'codec': b'DX10',
                       'flags': b'\x04\x00\x00\x00',
                       'head_flg': b'\x0f\x10\x02\x00',
                       'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'Y216': {'bpp': b'\x00\x00\x00\x00',
                       'codec': b'DX10',
                       'flags': b'\x04\x00\x00\x00',
                       'head_flg': b'\x0f\x10\x02\x00',
                       'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'Y410': {'bpp': b'\x00\x00\x00\x00',
                       'codec': b'DX10',
                       'flags': b'\x04\x00\x00\x00',
                       'head_flg': b'\x0f\x10\x02\x00',
                       'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'Y416': {'bpp': b'\x00\x00\x00\x00',
                       'codec': b'DX10',
                       'flags': b'\x04\x00\x00\x00',
                       'head_flg': b'\x0f\x10\x02\x00',
                       'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
              'YUY2': {'bpp': b'\x00\x00\x00\x00',
                       'codec': b'YUY2',
                       'flags': b'\x04\x00\x00\x00',
                       'head_flg': b'\x0f\x10\x02\x00',
                       'rgb_mask': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}
              }
