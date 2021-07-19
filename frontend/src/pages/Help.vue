<template>
  <div class="my-4 px-2">
    <p class="mt-8">
      N'hésitez surtout pas à me contacter ! Et par le moyen qui vous plaît le
      plus !
    </p>
    <div class="mt-4">
      <div class="flex items-center space-x-2">
        <IconPhone class="h-4 text-gray-700" />
        <p class="text-lg">
          Par Téléphone :
          <a class="font-bold text-teal-500" href="tel:+33698990069">
            +33 6 98 99 00 69
          </a>
        </p>
      </div>
      <p>(Appel, sms, Telegram, Signal, Whatsapp...)</p>
    </div>
    <div class="mt-4">
      <div class="flex items-center space-x-2">
        <IconMail class="h-4 text-gray-700" />
        <p class="text-lg">
          Par mail :
          <a class="font-bold text-teal-500" href="mailto:olivier@soklaki.fr">
            olivier@soklaki.fr
          </a>
        </p>
      </div>
    </div>
    <div class="mt-4">À tout bientôt ! 🤸</div>
  </div>
</template>

<script setup>
import IconPhone from "../icons/IconPhone.vue";
import IconMail from "../icons/IconMail.vue";
</script>
