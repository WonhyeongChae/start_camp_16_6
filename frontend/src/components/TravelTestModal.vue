<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { travelQuestions } from '../data/travelQuestions'

const emit = defineEmits(['complete', 'skip'])
const currentIndex = ref(0)
const answers = ref({})

const currentQuestion = computed(() => travelQuestions[currentIndex.value])
const selectedOptionId = computed(() => answers.value[currentQuestion.value.questionId])
const isLastQuestion = computed(() => currentIndex.value === travelQuestions.length - 1)
const progress = computed(() => ((currentIndex.value + 1) / travelQuestions.length) * 100)

function selectOption(optionId) {
  answers.value[currentQuestion.value.questionId] = optionId
}

function goNext() {
  if (!selectedOptionId.value) return
  if (isLastQuestion.value) {
    emit('complete', travelQuestions.map(({ questionId }) => ({ questionId, optionId: answers.value[questionId] })))
    return
  }
  currentIndex.value += 1
}

function goBack() {
  if (currentIndex.value > 0) currentIndex.value -= 1
}

function handleKeydown(event) {
  if (event.key === 'Enter' && selectedOptionId.value) goNext()
  if (event.key === 'Escape') emit('skip')
}

onMounted(() => {
  document.body.style.overflow = 'hidden'
  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="modal-backdrop" role="presentation">
    <section class="travel-modal" role="dialog" aria-modal="true" aria-labelledby="travel-question-title">
      <header class="modal-header">
        <div>
          <span class="eyebrow">나만의 여행 취향 찾기</span>
          <h2 id="travel-question-title">{{ currentQuestion.question }}</h2>
          <p>몇 가지 질문에 답하면 딱 맞는 구미·경북 여행지를 추천해드려요.</p>
        </div>
        <strong class="step">{{ currentIndex + 1 }} / {{ travelQuestions.length }}</strong>
      </header>

      <div class="progress-track" aria-label="진행률"><span :style="{ width: `${progress}%` }"></span></div>

      <div class="option-grid" role="radiogroup" :aria-label="currentQuestion.question">
        <button
          v-for="option in currentQuestion.options"
          :key="option.optionId"
          class="option-card"
          :class="{ selected: selectedOptionId === option.optionId }"
          type="button"
          role="radio"
          :aria-checked="selectedOptionId === option.optionId"
          @click="selectOption(option.optionId)"
        >
          <span class="option-icon" :class="`tone-${option.tone}`" aria-hidden="true">{{ option.icon }}</span>
          <span>{{ option.text }}</span>
          <span v-if="selectedOptionId === option.optionId" class="check" aria-hidden="true">✓</span>
        </button>
      </div>

      <footer class="modal-footer">
        <button class="skip-button" type="button" @click="emit('skip')">다음에 할게요</button>
        <div class="modal-actions">
          <button class="previous-button" type="button" :disabled="currentIndex === 0" @click="goBack">이전</button>
          <button class="next-button" type="button" :disabled="!selectedOptionId" @click="goNext">
            {{ isLastQuestion ? '결과 보기' : '다음' }}
          </button>
        </div>
      </footer>
      <p class="reassurance">결과는 언제든 다시 확인할 수 있어요.</p>
    </section>
  </div>
</template>

<style scoped>
.modal-backdrop { position: fixed; z-index: 100; inset: 0; display: grid; place-items: center; padding: 28px; background: rgba(13, 27, 36, .58); backdrop-filter: blur(7px); }
.travel-modal { width: min(730px, 100%); max-height: calc(100vh - 40px); overflow-y: auto; padding: 46px 58px 28px; background: #fff; border-radius: 20px; box-shadow: 0 30px 90px rgba(0,0,0,.22); }
.modal-header { display: grid; grid-template-columns: 1fr auto; gap: 20px; }
.eyebrow { display: block; margin-bottom: 8px; color: var(--green-900); font-size: 17px; font-weight: 800; }
.modal-header h2 { margin: 0; color: var(--navy); font-size: clamp(25px, 3vw, 34px); line-height: 1.3; letter-spacing: -1px; }
.modal-header p { margin: 12px 0 0; color: #626a66; font-size: 14px; }
.step { color: var(--navy); font-size: 16px; white-space: nowrap; }
.progress-track { height: 8px; margin: 28px 0 30px; overflow: hidden; background: #eef0ed; border-radius: 999px; }
.progress-track span { display: block; height: 100%; background: var(--green-900); border-radius: inherit; transition: width 220ms ease; }
.option-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.option-card { position: relative; min-height: 138px; display: grid; grid-template-columns: auto 1fr; align-items: center; gap: 18px; padding: 18px 20px; color: var(--navy); text-align: left; background: #fff; border: 1px solid #d7d9d6; border-radius: 13px; font-size: 16px; font-weight: 750; line-height: 1.6; transition: border-color 160ms, background 160ms, transform 160ms; }
.option-card:hover { transform: translateY(-2px); border-color: #7eae91; }
.option-card.selected { background: #f7fbf7; border: 1.5px solid var(--green-900); box-shadow: 0 0 0 3px rgba(7,92,58,.06); }
.option-icon { width: 64px; height: 64px; display: grid; place-items: center; border-radius: 50%; font-size: 28px; }
.tone-green { background: #e5f3d9; } .tone-blue { background: #e7f1fb; } .tone-purple { background: #f1ebf6; } .tone-orange { background: #fff0dc; }
.check { position: absolute; top: 10px; right: 12px; width: 22px; height: 22px; display: grid; place-items: center; color: #fff; background: var(--green-900); border-radius: 50%; font-size: 12px; }
.modal-footer { display: flex; align-items: center; justify-content: space-between; gap: 20px; margin-top: 30px; }
.skip-button { padding: 7px 0; color: #525b57; background: transparent; border-bottom: 1px solid #525b57; }
.modal-actions { display: flex; gap: 12px; }
.previous-button, .next-button { min-width: 104px; height: 45px; border-radius: 7px; font-weight: 800; }
.previous-button { color: var(--green-900); background: #fff; border: 1px solid var(--green-900); }
.next-button { color: #fff; background: var(--green-900); }
.previous-button:disabled, .next-button:disabled { opacity: .38; cursor: not-allowed; }
.reassurance { margin: 20px 0 0; color: #777d79; text-align: center; font-size: 12px; }
@media (max-width: 650px) {
  .modal-backdrop { padding: 12px; align-items: end; }
  .travel-modal { max-height: calc(100vh - 12px); padding: 28px 20px 20px; border-radius: 20px 20px 0 0; }
  .option-grid { grid-template-columns: 1fr; }
  .option-card { min-height: 90px; }
  .modal-footer { align-items: flex-end; }
  .modal-actions { width: 62%; }
  .previous-button, .next-button { min-width: 0; flex: 1; }
}
</style>
