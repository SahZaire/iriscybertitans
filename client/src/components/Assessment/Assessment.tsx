

import * as React from 'react';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Button from '@mui/material/Button';
import testPaperBackground from '../../assets/images/courses/testpaper2.jpg';

function createQuestion(
  questionText: string,
  optionA: string,
  optionB: string,
  optionC: string,
  optionD: string,
  correctOption: string,
) {
  return {
    questionText,
    optionA,
    optionB,
    optionC,
    optionD,
    correctOption,
    history: [
      {
        solution: 'this is sol..',
        // participantId: '11091700',
        // response: 'Correct',
      },
    ],
  };
}

function QuestionRow(props: { question: ReturnType<typeof createQuestion> }) {
  const { question } = props;
  const [open, setOpen] = React.useState(false);

  return (
    <React.Fragment>
      <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </TableCell>
        <TableCell component="th" scope="row">
          {question.questionText}
        </TableCell>
        <TableCell align="right">{question.optionA}</TableCell>
        <TableCell align="right">{question.optionB}</TableCell>
        <TableCell align="right">{question.optionC}</TableCell>
        <TableCell align="right">{question.optionD}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              <Typography variant="h6" gutterBottom component="div">
                Explanation
              </Typography>
              <Table size="small" aria-label="responses">
                <TableHead>
                  
                </TableHead>
                <TableBody>
                  {question.history.map((responseRow) => (
                    <TableRow key={responseRow.solution}>
                      <TableCell component="th" scope="row">
                        {responseRow.solution}
                      </TableCell>
                      {/* <TableCell>{responseRow.participantId}</TableCell> */}
                      {/* <TableCell align="right">{responseRow.response}</TableCell> */}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
}

const questions = [
  createQuestion('What is the primary function of a rectifier?', 'Signal amplification', 'Voltage regulation', 'Current transformation', 'AC to DC conversion', 'D'),
  createQuestion('Which material is commonly used as a semiconductor in electronics?', 'Copper', 'Silicon', 'Aluminum', 'Gold', 'B'),
  createQuestion('What does the term PID controller stand for in control systems?', 'Proportional Integral Derivative', 'Primary Input Device', 'Power Integrated Device', 'Programmable Interface Driver', 'A'),
  createQuestion('Which law states that the total electric flux through a closed surface is equal to the charge enclosed by the surface divided by the permittivity of free space?', 'Gauss\'s Law', 'Faraday\'s Law', 'Ohm\'s Law', 'Ampere\'s Law', 'A'),
  createQuestion('What is the purpose of a strain gauge in engineering applications?', 'Measure temperature', 'Measure pressure', 'Measure strain or deformation', 'Measure velocity', 'C'),
];

export default function QuizTable() {
  return (
    <div className='table-container' style={{ backgroundImage: `url(${testPaperBackground})`, backgroundSize: 'cover', backgroundPosition: 'center', backgroundRepeat: 'no-repeat' }}>
      <TableContainer sx={{ width: 800, background: 'snow' }} component={Paper}>
        <Table aria-label="quiz table">
          <TableHead>
            <TableRow>
              <TableCell />
              <TableCell><h2>Questions</h2></TableCell>
              <TableCell align="right"><h3>Option A</h3></TableCell>
              <TableCell align="right"><h3>Option B</h3></TableCell>
              <TableCell align="right"><h3>Option C</h3></TableCell>
              <TableCell align="right"><h3>Option D</h3></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {questions.map((question) => (
              <QuestionRow key={question.questionText} question={question} />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <br />
      <div style={{ width: 800, display: 'flex', justifyContent: 'space-around' }}>
        <Button sx={{ width: 350 }} color='secondary' variant="contained">Reset</Button>
        <Button sx={{ width: 350 }} variant="contained">Submit</Button>
      </div>
    </div>
  );
}
