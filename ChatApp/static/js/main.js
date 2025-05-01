// HTML内の<script>タグに配置
function showDeleteConfirm(childId) {
	// 値をセット
	document.getElementById('deleteChildId').value = childId;

	// ポップを表示
	document.getElementById('deleteConfirm').style.display = 'flex';
}

function hideDeleteConfirm() {
	// フォームの値をリセット
	document.getElementById('deleteChildId').value = '';
	// ポップアップをを非表示
	document.getElementById('deleteConfirm').style.display = 'none';
}