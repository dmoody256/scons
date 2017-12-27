
function Retry-Command
{
    param (
    [Parameter(Mandatory=$true)][string]$command, 
    [Parameter(Mandatory=$false)][hashtable]$args, 
    [Parameter(Mandatory=$false)][int]$retries = 5, 
    [Parameter(Mandatory=$false)][int]$secondsDelay = 2
    )
    
    # Setting ErrorAction to Stop is important. This ensures any errors that occur in the command are 
    # treated as terminating errors, and will be caught by the catch block.
    # $args.ErrorAction = "Stop"
    
    $retrycount = 0
    $completed = $false

    while (-not $completed) {
        try {
            & $command @args
            Write-Verbose ("Command [{0}] succeeded." -f $command)
            $completed = $true
        } catch {
            if ($retrycount -ge $retries) {
                Write-Verbose ("Command [{0}] failed the maximum number of {1} times." -f $command, $retrycount)
                throw
            } else {
                Write-Verbose ("Command [{0}] failed. Retrying in {1} seconds." -f $command, $secondsDelay)
                Start-Sleep $secondsDelay
                $retrycount++
            }
        }
    }
}

Retry-Command -Command "python runtest.py src/engine/SCons/JobTests.py" -Verbose

$TOTAL_BUILD_JOBS = 4;
$Lines = (Get-Content all_tests.txt | Measure-Object -line).Lines;
$start = ($Lines / $TOTAL_BUILD_JOBS) * ($Env:BUILD_JOB_NUM - 1);
$end = ($Lines / $TOTAL_BUILD_JOBS) * $Env:BUILD_JOB_NUM;
if ( $Env:BUILD_JOB_NUM -eq $TOTAL_BUILD_JOBS){ $end = $Lines };
if ( $start -eq 0 ){ $start = 1 };
get-content all_tests.txt | select -first ($end - $start) -skip ($start - 1) | Out-File -Encoding ASCII build_tests.txt;