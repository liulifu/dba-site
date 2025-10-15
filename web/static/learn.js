(function(){
  const stepsEl = document.getElementById('steps');
  const radio = document.querySelectorAll('input[name="auth"]');
  const tpl = (mode)=>{
    if(mode==='oidc'){
      return `
      <ol>
        <li>在 Azure AD 应用为 GitHub 仓库创建 Federated Credential（repo: liulifu/dba-site, branch: main）。</li>
        <li>在 GitHub Actions 工作流中使用 azure/login@v2（OIDC），无需存储长期密钥。</li>
        <li>推送到 main，流水线自动构建镜像并更新 Container Apps。</li>
      </ol>`;
    }
    return `
      <ol>
        <li>在 Azure 中创建 Service Principal，并记录 clientId/tenantId/subscriptionId/clientSecret。</li>
        <li>将上述 JSON 以 AZURE_CREDENTIALS Secret 形式保存到仓库。</li>
        <li>推送到 main，流水线使用 service principal 登录，构建并发布。</li>
      </ol>`;
  };
  function render(){
    const v = document.querySelector('input[name="auth"]:checked').value;
    stepsEl.innerHTML = tpl(v);
  }
  radio.forEach(r=>r.addEventListener('change', render));
  render();
})();

