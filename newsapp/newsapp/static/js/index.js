function goToCategory(select) {
  const categoryId = select.value;
  if (categoryId) {
    window.location.href = `/category/${categoryId}/`;  // 선택된 카테고리로 이동
  } else {
    window.location.href = `/`;  // 전체 보기
  }
}