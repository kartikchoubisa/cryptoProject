import React from 'react'

export default function Home() {
  let [isCertificateIssued1, setisCertificateIssued1] = React.useState(false)
  let [isCertificateIssued2, setisCertificateIssued2] = React.useState(false)
  let [username1, setUsername1] = React.useState('Arjun')
  let [username2, setUsername2] = React.useState('Bheem')

  async function generateCertificate(user) {
    // await fetch('localhost:5000/generate_certificate/{username}');
    if (user == "1") setisCertificateIssued1(true);
    else setisCertificateIssued2(true);
  }

  let [message, setMessage] = React.useState('')
  async function handleChange(e) {
    e.preventDefault;
    setMessage(e.target.value);
  }
  async function handleSend() {
    // await fetch('localhost:5000/send_message/{username}/{message}');
    setReceivedMessage(message);
    setVerified(false)
    setMessage('');
    setReceived(true);
  }

  let [received, setReceived] = React.useState(false)
  let [receivedMessage, setReceivedMessage] = React.useState('')
  let [verified, setVerified] = React.useState(false)
  async function verifyMessage() {
    // await fetch('localhost:5000/verify_message/{username}/{message}');
    setVerified(true);
  }

  return (
    <div> 
      <div className="m-8 flex">
        <div className={`w-[320px] p-8 mr-12 bg-primary rounded-2xl text-white`}>
          <img src="./User.svg" className='mb-2' />
          <div>{username1}</div>
          <div className='mb-8'> Certificate:
            {
              !isCertificateIssued1 ?
                <span className='text-gray-300'> Not Issued</span>
                : <span className='text-green-500'> Issued</span>
            }
          </div>
          {
            !isCertificateIssued1 ?
              <img src="./Button.svg" className='ml-auto mr-auto cursor-pointer' onClick={() => generateCertificate("1")} />
              :
              <div>
                <div className='text-[#A7C9E8] font-semibold text-sm mb-2'>Message</div>
                <div className='flex'>
                  <input className='rounded-lg h-4 p-4 w-48 mr-4 text-black' onChange={(e) => handleChange(e)} value={message}></input>
                  <img src="./Send.svg" className='cursor-pointer' onClick={handleSend} />
                </div>
              </div>
          }
        </div>


        <div className={`w-[320px] p-8 bg-primary rounded-2xl text-white`}>
          <img src="./User.svg" className='mb-2' />
          <div>{username2}</div>
          <div className='mb-8'> Certificate:
            {
              !isCertificateIssued2 ?
                <span className='text-gray-300'> Not Issued</span>
                : <span className='text-green-500'> Issued</span>
            }
          </div>
          {
            !isCertificateIssued2 ?
              <img src="./Button.svg" className='ml-auto mr-auto cursor-pointer' onClick={() => generateCertificate("2")} />
              :
              <div>
                {
                  received ?
                  <div>
                    <div>

                    {
                      verified ?
                      <span className='text-green-500 font-semibold text-sm mb-2'>Verified! </span>
                      :
                      <span className='text-[#F5A623] font-semibold text-sm mb-2'>Received </span>
                    }
                    <span>{receivedMessage}</span>
                    </div>
                    <img src="./Verify.svg" className='ml-auto mr-auto cursor-pointer mt-2' onClick={verifyMessage}/>
                  </div>
                  :
                  <img src="./VerifyGray.svg" className='ml-auto mr-auto cursor-pointer'/>
                }
              </div>
          }
        </div>


      </div>
    </div>
  )
}
