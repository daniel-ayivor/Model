# rename_folders.ps1
$targetDir = "./plant_datasets/processed/train"

if (Test-Path $targetDir) {
    # Get all subdirectories in the train folder
    $folders = Get-ChildItem -Path $targetDir -Directory
    
    foreach ($folder in $folders) {
        $oldName = $folder.Name
        
        # 1. Replace PlantVillage style '___' or '__' with a single underscore
        # 2. Replace brackets, parentheses, and spaces with underscores
        $newName = $oldName -replace '___', '_' -replace '__', '_' -replace '\s+', '_'
        $newName = $newName -replace '\(', '' -replace '\)', '' -replace '-', '_'
        
        # 3. Convert the entire string to lowercase
        $newName = $newName.ToLower()
        
        # Clean up any accidental double underscores left over from the merges
        $newName = $newName -replace '__', '_'
        $newName = $newName.Trim('_')

        # Only rename if the name actually needs changing
        if ($oldName -ne $newName) {
            $oldPath = $folder.FullName
            $newPath = Join-Path $folder.Parent.FullName $newName
            
            # If the destination folder already exists, move files into it instead of crashing
            if (Test-Path $newPath) {
                Write-Host "Merging images from [$oldName] into existing folder [$newName]..." -ForegroundColor Yellow
                Move-Item -Path "$oldPath\*" -Destination $newPath -Force -ErrorAction SilentlyContinue
                Remove-Item -Path $oldPath -Recurse -Force
            } else {
                Write-Host "Renaming: $oldName  -->  $newName" -ForegroundColor Green
                Rename-Item -Path $oldPath -NewName $newName
            }
        }
    }
    Write-Host "`nAll folders processed successfully!" -ForegroundColor Cyan
} else {
    Write-Host "Error: Directory $targetDir not found!" -ForegroundColor Red
}