import { defineConfig } from 'vite'

import vue from '@vitejs/plugin-vue'

import vueJsx from '@vitejs/plugin-vue-jsx'

import AutoImport from 'unplugin-auto-import/vite'

import Components from 'unplugin-vue-components/vite'

import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'


export default defineConfig({

  // 
  plugins: [

    vue(),

    vueJsx(),

    AutoImport({

      imports: [
        'vue', 
        'vue-router',
      ],

      resolvers: [
        ElementPlusResolver()
      ],

      // dir: [
      //   './src/components/',
      // ]

    }),

    Components({

      dirs: [
        './src/components/'
      ],

      resolvers: [
        ElementPlusResolver()
      ],
    }),
  ],

})
