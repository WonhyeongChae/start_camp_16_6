<template>
  <div v-if="show" class="overlay" @click.self="handleBackdrop">
    <div class="modal">
      <template v-if="!isTestFinished">
        <h2>여행 유형 테스트</h2>
        <p>간단한 테스트 템플릿입니다. 실제 질문은 백엔드/문서에서 연결하세요.</p>

        <form @submit.prevent="handleSubmit">
          <div v-for="(q, qi) in questions" :key="q.questionId" class="question">
            <h3>{{ qi + 1 }}. {{ q.text }}</h3>
            <div class="options">
              <label v-for="opt in q.options" :key="opt.optionId" class="option">
                <input
                  type="radio"
                  :name="`q-${q.questionId}`"
                  :value="opt.optionId"
                  v-model="answers[q.questionId]"
                  required
                />
                <span>{{ opt.text }}</span>
              </label>
            </div>
          </div>

          <div class="actions">
            <button type="submit" class="btn-primary">제출</button>
            <button type="button" class="btn-secondary" @click="closeModal">취소</button>
          </div>
        </form>
      </template>

      <template v-else>
        <h2>결과 확인</h2>
        <p>당신의 여행 유형은 <strong>{{ result.name }}</strong>입니다.</p>
        <p class="result-desc">{{ result.description }}</p>

        <div class="actions">
          <button class="btn-primary" @click="finalClose">닫기</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const props = defineProps({
  show: { type: Boolean, default: false }
})
const emit = defineEmits(['update:show', 'submit-result'])

/*
 - isTestFinished: 내부 화면 전환 플래그
 - answers: { questionId: selectedOptionId, ... }
 - questions: 경량 템플릿(문서 기반). 나중에 API로 교체하기 쉽게 구조화.
*/
const isTestFinished = ref(false)
const answers = reactive({})

const questions = [
  {
    questionId: 1,
    text: '여행에서 가장 기대되는 순간은?',
    options: [
      { optionId: 'Q1_A', text: '자연 속에서 여유롭게 쉬기', type: 'HEALING' },
      { optionId: 'Q1_B', text: '체험과 액티비티', type: 'EXPLORER' },
      { optionId: 'Q1_C', text: '역사·문화 탐방', type: 'CULTURE' },
      { optionId: 'Q1_D', text: '지역 음식 즐기기', type: 'FOODIE' }
    ]
  },
  {
    questionId: 2,
    text: '3시간의 자유시간이 생긴다면?',
    options: [
      { optionId: 'Q2_A', text: '공원 산책', type: 'HEALING' },
      { optionId: 'Q2_B', text: '액티비티 참여', type: 'EXPLORER' },
      { optionId: 'Q2_C', text: '전시/박물관', type: 'CULTURE' },
      { optionId: 'Q2_D', text: '시장·맛집 탐방', type: 'FOODIE' }
    ]
  },
  {
    questionId: 3,
    text: '여행 후 오래 기억에 남는 것은?',
    options: [
      { optionId: 'Q3_A', text: '편안한 분위기', type: 'HEALING' },
      { optionId: 'Q3_B', text: '활동적 경험', type: 'EXPLORER' },
      { optionId: 'Q3_C', text: '장소의 이야기', type: 'CULTURE' },
      { optionId: 'Q3_D', text: '인상 깊은 음식', type: 'FOODIE' }
    ]
  }
]

// 임시 결과 구조: code, name(한글), description
const result = reactive({ code: '', name: '', description: '' })

function handleBackdrop() {
  // 백드롭 클릭 시 닫지 않게 원하는 경우 주석 유지.
  // closeModal()
}

function handleSubmit() {
  // 간단한 클라이언트 사이드 집계(임시)
  const score = { HEALING: 0, EXPLORER: 0, CULTURE: 0, FOODIE: 0 }

  questions.forEach(q => {
    const sel = answers[q.questionId]
    const opt = q.options.find(o => o.optionId === sel)
    if (opt) score[opt.type] += 1
  })

  // 최다 득표 타입 선택(동점은 순서 HEALING->EXPLORER->CULTURE->FOODIE 우선)
  const order = ['HEALING', 'EXPLORER', 'CULTURE', 'FOODIE']
  let max = -1
  let chosen = 'HEALING'
  order.forEach(k => {
    if (score[k] > max) {
      max = score[k]
      chosen = k
    } else if (score[k] === max && max !== -1) {
      // keep existing chosen per order priority
    }
  })

  // 간단한 한글 명칭/설명(문서의 표시 원칙에 따름)
  const map = {
    HEALING: { name: '고요한 쉼표 수집가', description: '자연 속에서 여유를 즐기는 유형입니다.' },
    EXPLORER: { name: '에너지 만렙 탐험가', description: '체험과 야외 활동을 선호하는 유형입니다.' },
    CULTURE: { name: '이야기를 좇는 시간여행자', description: '역사와 문화를 즐기는 유형입니다.' },
    FOODIE: { name: '한입에 담는 로컬 미식가', description: '음식과 시장을 중심으로 여행하는 유형입니다.' }
  }

  result.code = chosen
  result.name = map[chosen].name
  result.description = map[chosen].description

  // 화면 전환: 결과 뷰로 이동하지만 모달은 열려있음
  isTestFinished.value = true

  // FE는 실제로는 BE에 결과 전송하거나, BE가 결과를 계산함.
  // 여기서는 UI 검증을 위해 임시 계산을 사용.
}

function finalClose() {
  // 부모에게 결과 전달하고 모달 닫기
  emit('submit-result', { code: result.code, name: result.name })
  emit('update:show', false)
  // 리셋 (원하면)
  reset()
}

function closeModal() {
  emit('update:show', false)
  reset()
}

function reset() {
  isTestFinished.value = false
  Object.keys(answers).forEach(k => delete answers[k])
  result.code = ''
  result.name = ''
  result.description = ''
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.45);
  z-index: 1000;
}
.modal {
  width: 92%;
  max-width: 640px;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}
.question { margin-bottom: 16px; }
.options { display: flex; flex-direction: column; gap: 8px; margin-top: 8px; }
.option input { margin-right: 8px; }
.actions { display: flex; gap: 12px; margin-top: 16px; }
.btn-primary { padding: 8px 12px; background: #1976d2; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
.btn-secondary { padding: 8px 12px; background: #eee; color: #333; border: none; border-radius: 6px; cursor: pointer; }
.result-desc { color: #444; margin-top: 8px; }
</style>